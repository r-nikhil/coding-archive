import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

from rag_service import RAGService
from openai_service import OpenAIService
from analytics import Analytics
from content_filter import ContentFilter
from conversation_history import ConversationHistory
from webhook_service import WebhookService
from admin_panel import AdminPanel
from db_services import db_conversation_service, db_analytics_service, db_webhook_service, db_admin_service
from database import db_manager

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Enable CORS for GitHub Pages
CORS(app, origins=["*"])

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
limiter.init_app(app)

# Initialize services
rag_service = RAGService()
openai_service = OpenAIService()
analytics = Analytics()
content_filter = ContentFilter()
conversation_history = ConversationHistory()
webhook_service = WebhookService()

# Initialize admin panel (must be done after app creation)
admin_panel = AdminPanel(app, analytics, conversation_history, webhook_service, rag_service, openai_service)

# Initialize RAG service on startup
try:
    rag_service.initialize()
    logger.info("RAG service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize RAG service: {e}")

# In-memory storage for user chat counts (in production, use Redis)
user_chat_counts = {}

@app.route('/', methods=['GET'])
def home():
    """Homepage with API documentation"""
    return jsonify({
        "message": "Nikhil's AI-Powered Chatbot Backend",
        "description": "Flask backend with RAG capabilities, conversation history, webhooks, and admin panel",
        "base_url": "https://llm-chat-backend-NikhilR24.replit.app",
        "documentation": {
            "interactive": "https://llm-chat-backend-NikhilR24.replit.app/docs",
            "markdown": "See api_docs.md for complete documentation"
        },
        "api_endpoints": {
            "chat": "POST /api/chat - Main chat interface",
            "health": "GET /api/health - System health check",
            "conversations": "GET /api/conversations/recent - Get recent conversations",
            "analytics": "GET /api/analytics/summary - Analytics summary",
            "admin": "GET /admin/login - Admin panel login"
        },
        "features": [
            "RAG with ChromaDB and OpenAI embeddings",
            "Conversation history with context awareness", 
            "Real-time webhooks for integrations",
            "Comprehensive admin panel",
            "Advanced analytics and monitoring",
            "Content filtering and rate limiting"
        ],
        "version": "1.0.0",
        "status": "operational"
    })

@app.route('/docs', methods=['GET'])
def documentation():
    """Interactive API documentation"""
    try:
        with open('api_docs.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        from flask import Response
        return Response(html_content, mimetype='text/html')
    except FileNotFoundError:
        logger.error("api_docs.html file not found")
        return jsonify({"error": "Documentation not found"}), 404
    except Exception as e:
        logger.error(f"Error serving documentation: {e}")
        return jsonify({"error": "Failed to load documentation"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Basic health checks
        status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "rag": rag_service.is_healthy(),
                "openai": openai_service.is_healthy(),
                "analytics": analytics.is_healthy(),
                "conversation_history": conversation_history.is_healthy(),
                "webhook_service": webhook_service.is_healthy(),
                "database": db_manager.health_check()
            }
        }
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    """Main chat endpoint with RAG integration"""
    try:
        # Get request data
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        timestamp = data.get('timestamp', datetime.utcnow().isoformat())
        user_ip = get_remote_address()
        
        # Input validation and sanitization
        if not user_message.strip():
            return jsonify({"error": "Empty message not allowed"}), 400
        
        if len(user_message) > 1000:
            return jsonify({"error": "Message too long. Please keep it under 1000 characters."}), 400
        
        # Content filtering
        if not content_filter.is_safe(user_message):
            db_analytics_service.log_filtered_request(user_ip, user_message)
            return jsonify({"error": "Message contains inappropriate content"}), 400
        
        # Check user chat limit
        if user_ip not in user_chat_counts:
            user_chat_counts[user_ip] = 0
        
        if user_chat_counts[user_ip] >= 10:
            return jsonify({
                "error": "You've reached the maximum number of chats. Please email contact@rnikhil.com to chat directly. OpenAI credits are expensive!"
            }), 429
        
        # Increment user chat count
        user_chat_counts[user_ip] += 1
        
        # Handle conversation history
        conversation_id = data.get('conversation_id')
        if not conversation_id:
            conversation_id = db_conversation_service.create_conversation(user_ip)
        
        # Get conversation context for better responses
        conversation_context = db_conversation_service.get_conversation_context(conversation_id)
        
        # Retrieve relevant content using RAG
        relevant_content = rag_service.search_relevant_content(user_message)
        
        # Generate response using OpenAI with conversation context
        response_text = openai_service.generate_response(user_message, relevant_content, conversation_context)
        
        # Save to conversation history
        db_conversation_service.add_message(conversation_id, user_message, response_text, timestamp)
        
        # Log the interaction
        db_analytics_service.log_chat_interaction(user_ip, conversation_id, user_message, response_text)
        
        # Trigger webhook for new message
        webhook_service.trigger_webhook("new_message", {
            "conversation_id": conversation_id,
            "user_ip": user_ip,
            "message": user_message,
            "response": response_text,
            "timestamp": timestamp
        })
        
        response_data = {
            "response": response_text,
            "timestamp": datetime.utcnow().isoformat(),
            "conversation_id": conversation_id
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        analytics.log_error(user_ip if 'user_ip' in locals() else 'unknown', str(e))
        
        # Trigger webhook for errors
        webhook_service.trigger_webhook("error", {
            "error": str(e),
            "user_ip": user_ip if 'user_ip' in locals() else 'unknown',
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return jsonify({"error": "Internal server error. Please try again later."}), 500

# Additional API endpoints for conversation history
@app.route('/api/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history by ID"""
    try:
        conversation = db_conversation_service.get_conversation(conversation_id)
        if conversation:
            return jsonify(conversation), 200
        else:
            return jsonify({"error": "Conversation not found"}), 404
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/conversations/recent', methods=['GET'])
def get_recent_conversations():
    """Get recent conversations"""
    try:
        limit = int(request.args.get('limit', 10))
        conversations = db_conversation_service.get_recent_conversations(limit)
        return jsonify(conversations), 200
    except Exception as e:
        logger.error(f"Error getting recent conversations: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Analytics API endpoints
@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    try:
        summary = db_analytics_service.get_analytics_summary()
        return jsonify(summary), 200
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(429)
def rate_limit_handler(e):
    """Rate limit error handler"""
    return jsonify({
        "error": "Rate limit exceeded. Please wait before sending another message."
    }), 429

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    # Log the request details for debugging
    logger.warning(f"404 error for {request.method} {request.path} from {request.remote_addr}")
    return jsonify({
        "error": "Endpoint not found", 
        "message": f"The requested URL '{request.path}' was not found on the server.",
        "available_endpoints": [
            "GET / - API overview",
            "GET /docs - Interactive documentation", 
            "GET /api/health - Health check",
            "POST /api/chat - Chat interface",
            "GET /api/conversations/recent - Recent conversations",
            "GET /api/analytics/summary - Analytics",
            "GET /admin/login - Admin panel"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """500 error handler"""
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Initialize RAG service on startup
    try:
        rag_service.initialize()
        logger.info("RAG service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
