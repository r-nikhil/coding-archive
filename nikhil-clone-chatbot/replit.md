# AI-Powered Personal Chatbot Backend

## Overview

This is a comprehensive Flask-based backend for an AI-powered chatbot that serves a personal website's chat interface. The system combines Retrieval-Augmented Generation (RAG) with OpenAI's GPT-4o to provide personalized responses about AI, investing, poker, and other topics based on blog content. The backend includes advanced features like conversation history, real-time webhooks, comprehensive analytics dashboard, and a full admin panel for system management. The backend is designed to be deployed on Replit and serve a GitHub Pages frontend.

## System Architecture

### Core Components
- **Flask Application**: Main web server with CORS support for cross-origin requests
- **RAG Service**: Handles document processing, embedding generation, and semantic search
- **OpenAI Service**: Manages GPT-4o API interactions and response generation with conversation context
- **Conversation History**: Persistent storage and management of chat conversations
- **Webhook Service**: Real-time event notifications and integrations
- **Admin Panel**: Comprehensive management interface with authentication
- **Analytics**: Advanced usage tracking with detailed statistics and reporting
- **Content Filter**: Provides safety guardrails against inappropriate content and prompt injection
- **Rate Limiting**: Prevents API abuse with configurable limits

### Technology Stack
- **Backend Framework**: Flask with CORS
- **Database**: PostgreSQL with SQLAlchemy ORM for persistent data storage
- **Vector Database**: ChromaDB for RAG embeddings storage
- **LLM**: OpenAI GPT-4o with text-embedding-ada-002 for embeddings
- **Document Processing**: Python-frontmatter for markdown parsing
- **Rate Limiting**: Flask-Limiter with IP-based tracking
- **Security**: Input validation, content filtering, and token usage limits

## Key Components

### 1. RAG Service (`rag_service.py`)
- Processes markdown files from `blog_posts/` directory
- Generates embeddings using OpenAI's text-embedding-ada-002
- Stores embeddings in ChromaDB with persistent storage
- Implements semantic search for relevant content retrieval
- Handles markdown frontmatter parsing for metadata extraction

### 2. OpenAI Service (`openai_service.py`)
- Manages GPT-4o API interactions with conversation context support
- Loads system prompt from external file (`system_prompt.txt`)
- Formats user messages with RAG context and conversation history
- Implements token usage limits and response length controls
- Handles API error scenarios gracefully

### 3. Conversation History (`conversation_history.py` + Database)
- PostgreSQL-backed persistent storage of conversation threads with unique IDs
- Context-aware responses using conversation history
- Database models: Conversation, Message tables with relationships
- Conversation management and cleanup utilities
- Real-time statistics tracking for conversation analytics

### 4. Webhook Service (`webhook_service.py`)
- Real-time event notifications for integrations
- Configurable webhook endpoints with secret validation
- Event types: new_message, message_filtered, error
- HMAC signature verification for security
- Comprehensive logging and success/failure tracking

### 5. Admin Panel (`admin_panel.py`)
- Web-based management interface with Bootstrap styling
- Token-based authentication for secure access
- Real-time system health monitoring
- Conversation history browsing and management
- Webhook configuration and monitoring
- System settings and prompt reloading capabilities

### 6. Analytics (`analytics.py` + Database)
- PostgreSQL-backed advanced usage tracking with conversation statistics
- Daily/historical analytics with trend analysis stored in database
- Popular topics extraction and monitoring
- Error tracking and performance metrics
- Database models: Analytics, ChatLog tables for comprehensive data storage

### 7. Content Filter (`content_filter.py`)
- Detects inappropriate content using regex patterns
- Prevents prompt injection attempts
- Blocks NSFW content and harmful language
- Provides safety guardrails with violation reason reporting

### 8. Flask Application (`app.py`)
- Main chat endpoint with conversation history support
- Additional API endpoints for conversation and analytics access
- Admin panel integration with authentication
- Rate limiting: 10 requests per minute per IP
- User chat limits: 10 chats per user session
- CORS configuration for GitHub Pages frontend
- Comprehensive error handling with webhook notifications

## Data Flow

1. **User Query**: Frontend sends POST request to `/api/chat` with optional conversation_id
2. **Input Validation**: Content filter checks for inappropriate content
3. **Rate Limiting**: Flask-Limiter enforces usage limits
4. **Conversation Management**: Create or retrieve conversation history
5. **RAG Retrieval**: RAG service finds relevant blog content using semantic search
6. **Context Preparation**: Combine conversation history with RAG context
7. **LLM Processing**: OpenAI service generates response with full context
8. **Storage**: Save message to conversation history
9. **Analytics**: Usage statistics are recorded
10. **Webhooks**: Trigger real-time notifications for integrations
11. **Response**: JSON response with conversation_id sent back to frontend

## API Endpoints

### Core Chat API
- `POST /api/chat` - Main chat interface with conversation history support
- `GET /api/health` - System health check with all service status

### Conversation Management
- `GET /api/conversation/<id>` - Retrieve specific conversation history
- `GET /api/conversations/recent` - Get recent conversations (with limit parameter)

### Analytics
- `GET /api/analytics/summary` - Comprehensive analytics summary

### Admin Panel
- `GET /admin/login` - Admin authentication interface
- `GET /admin/dashboard` - Real-time system monitoring dashboard
- `GET /admin/api/stats` - Detailed system statistics
- `POST /admin/api/webhooks` - Webhook management
- `POST /admin/api/system/reload-prompt` - Reload system prompt

## External Dependencies

### Required Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for GPT-4o and embeddings
- `SESSION_SECRET`: Flask session secret key (optional, defaults to dev key)

### Key Python Packages
- `flask`: Web framework
- `flask-cors`: Cross-origin resource sharing
- `flask-limiter`: Rate limiting
- `sqlalchemy`: Database ORM for PostgreSQL
- `psycopg2-binary`: PostgreSQL database adapter
- `openai`: OpenAI API client
- `chromadb`: Vector database for embeddings
- `python-frontmatter`: Markdown frontmatter parsing
- `werkzeug`: WSGI utilities

## Deployment Strategy

### Replit Configuration
- Main entry point: `main.py`
- Server runs on host `0.0.0.0`, port `5000`
- Debug mode enabled for development
- ProxyFix middleware for proper IP handling behind proxies

### Directory Structure
```
/
├── app.py                   # Main Flask application with all endpoints
├── main.py                  # Entry point with database initialization
├── models.py               # SQLAlchemy database models
├── database.py             # Database connection and management
├── db_services.py          # Database-backed service implementations
├── rag_service.py           # RAG implementation with ChromaDB
├── openai_service.py        # OpenAI integration with conversation context
├── conversation_history.py  # Legacy file-based conversation management
├── webhook_service.py       # Real-time event notifications
├── admin_panel.py          # Web-based admin interface
├── analytics.py            # Legacy file-based analytics
├── content_filter.py       # Safety guardrails and content validation
├── system_prompt.txt       # Editable system prompt
├── api_docs.html           # Interactive API documentation
├── api_docs.md             # Markdown API documentation
├── blog_posts/             # Markdown content directory
├── data/                   # ChromaDB persistent storage
└── (legacy file directories maintained for compatibility)
```

### Security Considerations
- Rate limiting prevents API abuse
- Content filtering blocks inappropriate requests
- Token usage limits control costs
- Input sanitization prevents injection attacks
- CORS configured for specific frontend origin

## Changelog
- July 08, 2025: Initial setup with core RAG and OpenAI integration
- July 08, 2025: Added conversation history with persistent storage and context-aware responses
- July 08, 2025: Implemented webhook service for real-time event notifications
- July 08, 2025: Created comprehensive admin panel with authentication and monitoring
- July 08, 2025: Enhanced analytics with conversation statistics and trend analysis
- July 08, 2025: Generated comprehensive API documentation (HTML + Markdown formats)
- July 08, 2025: **Integrated PostgreSQL database with SQLAlchemy ORM**
  - Created database models for conversations, messages, analytics, webhooks
  - Migrated from file-based storage to database-backed services
  - Improved data integrity and query performance
  - Added database health monitoring to health check endpoint

## User Preferences

Preferred communication style: Simple, everyday language.