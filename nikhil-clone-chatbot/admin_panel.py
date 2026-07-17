import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from flask import Blueprint, request, jsonify, render_template_string
import hashlib
import secrets

class AdminPanel:
    def __init__(self, app, analytics, conversation_history, webhook_service, rag_service, openai_service):
        self.app = app
        self.analytics = analytics
        self.conversation_history = conversation_history
        self.webhook_service = webhook_service
        self.rag_service = rag_service
        self.openai_service = openai_service
        
        self.admin_config_file = "admin_config.json"
        self.admin_config = self._load_admin_config()
        
        # Create admin blueprint
        self.admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
        self._setup_routes()
        
        # Register blueprint
        app.register_blueprint(self.admin_bp)
    
    def _load_admin_config(self) -> Dict[str, Any]:
        """Load admin configuration"""
        if os.path.exists(self.admin_config_file):
            try:
                with open(self.admin_config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading admin config: {e}")
        
        # Default config
        default_config = {
            "admin_token": secrets.token_urlsafe(32),
            "created_at": datetime.now().isoformat(),
            "rate_limits": {
                "requests_per_minute": 10,
                "chats_per_user": 10
            },
            "system_settings": {
                "max_response_length": 300,
                "rag_results_count": 3,
                "conversation_context_length": 5
            }
        }
        
        self._save_admin_config(default_config)
        return default_config
    
    def _save_admin_config(self, config: Dict[str, Any]):
        """Save admin configuration"""
        try:
            with open(self.admin_config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.admin_config = config
        except Exception as e:
            print(f"Error saving admin config: {e}")
    
    def _verify_admin_token(self, token: str) -> bool:
        """Verify admin token"""
        return token == self.admin_config.get("admin_token")
    
    def _setup_routes(self):
        """Setup admin panel routes"""
        
        @self.admin_bp.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                token = request.json.get('token')
                if self._verify_admin_token(token):
                    return jsonify({"success": True, "message": "Login successful"})
                else:
                    return jsonify({"success": False, "message": "Invalid token"}), 401
            
            return render_template_string(self._get_login_template())
        
        @self.admin_bp.route('/dashboard')
        def dashboard():
            # For GET requests to dashboard, we'll let the JavaScript handle auth
            # since the token is stored in localStorage
            return render_template_string(self._get_dashboard_template())
        
        @self.admin_bp.route('/api/stats')
        def get_stats():
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not self._verify_admin_token(token):
                return jsonify({"error": "Unauthorized"}), 401
            
            try:
                # Get comprehensive stats
                analytics_stats = self.analytics.get_analytics_summary()
                conversation_stats = self.conversation_history.get_conversation_stats()
                webhook_stats = self.webhook_service.get_webhook_stats()
                
                # System health
                system_health = {
                    "analytics": self.analytics.is_healthy(),
                    "conversation_history": self.conversation_history.is_healthy(),
                    "webhook_service": self.webhook_service.is_healthy(),
                    "rag_service": self.rag_service.is_healthy(),
                    "openai_service": self.openai_service.is_healthy()
                }
                
                return jsonify({
                    "analytics": analytics_stats,
                    "conversations": conversation_stats,
                    "webhooks": webhook_stats,
                    "system_health": system_health,
                    "timestamp": datetime.now().isoformat()
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.admin_bp.route('/api/conversations')
        def get_conversations():
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not self._verify_admin_token(token):
                return jsonify({"error": "Unauthorized"}), 401
            
            try:
                limit = int(request.args.get('limit', 20))
                conversations = self.conversation_history.get_recent_conversations(limit)
                return jsonify(conversations)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.admin_bp.route('/api/conversation/<conversation_id>')
        def get_conversation(conversation_id):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not self._verify_admin_token(token):
                return jsonify({"error": "Unauthorized"}), 401
            
            try:
                conversation = self.conversation_history.get_conversation(conversation_id)
                if conversation:
                    return jsonify(conversation)
                else:
                    return jsonify({"error": "Conversation not found"}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.admin_bp.route('/api/webhooks', methods=['GET', 'POST'])
        def manage_webhooks():
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not self._verify_admin_token(token):
                return jsonify({"error": "Unauthorized"}), 401
            
            if request.method == 'GET':
                return jsonify(self.webhook_service.get_webhook_stats())
            
            elif request.method == 'POST':
                data = request.json
                try:
                    webhook_id = self.webhook_service.add_webhook(
                        url=data['url'],
                        events=data['events'],
                        secret=data.get('secret'),
                        name=data.get('name')
                    )
                    return jsonify({"success": True, "webhook_id": webhook_id})
                except Exception as e:
                    return jsonify({"error": str(e)}), 400
        
        @self.admin_bp.route('/api/webhooks/<webhook_id>', methods=['DELETE', 'PUT'])
        def modify_webhook(webhook_id):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not self._verify_admin_token(token):
                return jsonify({"error": "Unauthorized"}), 401
            
            if request.method == 'DELETE':
                success = self.webhook_service.remove_webhook(webhook_id)
                return jsonify({"success": success})
            
            elif request.method == 'PUT':
                data = request.json
                success = self.webhook_service.toggle_webhook(webhook_id, data.get('active', True))
                return jsonify({"success": success})
        
        @self.admin_bp.route('/api/system/reload-prompt', methods=['POST'])
        def reload_system_prompt():
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not self._verify_admin_token(token):
                return jsonify({"error": "Unauthorized"}), 401
            
            try:
                self.openai_service.reload_system_prompt()
                return jsonify({"success": True, "message": "System prompt reloaded"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.admin_bp.route('/api/system/settings', methods=['GET', 'POST'])
        def manage_system_settings():
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not self._verify_admin_token(token):
                return jsonify({"error": "Unauthorized"}), 401
            
            if request.method == 'GET':
                return jsonify(self.admin_config.get("system_settings", {}))
            
            elif request.method == 'POST':
                data = request.json
                self.admin_config["system_settings"].update(data)
                self._save_admin_config(self.admin_config)
                return jsonify({"success": True, "settings": self.admin_config["system_settings"]})
    
    def _get_login_template(self) -> str:
        """Get login page template"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Panel - Login</title>
            <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
            <style>
                body { background-color: #1a1a1a; }
                .login-container { max-width: 400px; margin: 100px auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="login-container">
                    <div class="card">
                        <div class="card-header">
                            <h3>Admin Panel Login</h3>
                        </div>
                        <div class="card-body">
                            <form id="loginForm">
                                <div class="mb-3">
                                    <label for="token" class="form-label">Admin Token</label>
                                    <input type="password" class="form-control" id="token" required>
                                </div>
                                <button type="submit" class="btn btn-primary">Login</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                document.getElementById('loginForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const token = document.getElementById('token').value;
                    
                    try {
                        const response = await fetch('/admin/login', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ token })
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            localStorage.setItem('adminToken', token);
                            window.location.href = '/admin/dashboard';
                        } else {
                            alert('Invalid token');
                        }
                    } catch (error) {
                        alert('Login failed');
                    }
                });
            </script>
        </body>
        </html>
        '''
    
    def _get_dashboard_template(self) -> str:
        """Get dashboard template"""
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Panel - Dashboard</title>
            <link href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css" rel="stylesheet">
            <style>
                body { background-color: #1a1a1a; }
                .stat-card { margin-bottom: 20px; }
                .health-indicator { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 5px; }
                .health-healthy { background-color: #28a745; }
                .health-unhealthy { background-color: #dc3545; }
                .refresh-btn { position: fixed; top: 20px; right: 20px; }
            </style>
        </head>
        <body>
            <div class="container-fluid">
                <button class="btn btn-secondary refresh-btn" onclick="loadStats()">Refresh</button>
                
                <h1>Admin Dashboard</h1>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card stat-card">
                            <div class="card-header">
                                <h5>System Health</h5>
                            </div>
                            <div class="card-body" id="systemHealth">
                                Loading...
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card stat-card">
                            <div class="card-header">
                                <h5>Analytics Summary</h5>
                            </div>
                            <div class="card-body" id="analyticsStats">
                                Loading...
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="card stat-card">
                            <div class="card-header">
                                <h5>Conversation Stats</h5>
                            </div>
                            <div class="card-body" id="conversationStats">
                                Loading...
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-6">
                        <div class="card stat-card">
                            <div class="card-header">
                                <h5>Webhook Stats</h5>
                            </div>
                            <div class="card-body" id="webhookStats">
                                Loading...
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">
                                <h5>Recent Conversations</h5>
                            </div>
                            <div class="card-body" id="recentConversations">
                                Loading...
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="row mt-4">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header">
                                <h5>System Actions</h5>
                            </div>
                            <div class="card-body">
                                <button class="btn btn-warning" onclick="reloadSystemPrompt()">Reload System Prompt</button>
                                <button class="btn btn-secondary" onclick="exportData()">Export Data</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                const token = localStorage.getItem('adminToken');
                if (!token) {
                    window.location.href = '/admin/login';
                }
                
                const headers = {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                };
                
                async function loadStats() {
                    try {
                        const response = await fetch('/admin/api/stats', { headers });
                        const data = await response.json();
                        
                        if (response.ok) {
                            updateSystemHealth(data.system_health);
                            updateAnalyticsStats(data.analytics);
                            updateConversationStats(data.conversations);
                            updateWebhookStats(data.webhooks);
                            loadRecentConversations();
                        } else if (response.status === 401) {
                            localStorage.removeItem('adminToken');
                            window.location.href = '/admin/login';
                        } else {
                            alert('Failed to load stats: ' + data.error);
                        }
                    } catch (error) {
                        console.error('Error loading stats:', error);
                        alert('Network error loading stats');
                    }
                }
                
                function updateSystemHealth(health) {
                    const html = Object.entries(health).map(([service, healthy]) => 
                        `<div><span class="health-indicator ${healthy ? 'health-healthy' : 'health-unhealthy'}"></span>${service}: ${healthy ? 'Healthy' : 'Unhealthy'}</div>`
                    ).join('');
                    document.getElementById('systemHealth').innerHTML = html;
                }
                
                function updateAnalyticsStats(stats) {
                    const html = `
                        <div>Total Chats: ${stats.total_chats}</div>
                        <div>Unique Users: ${stats.unique_users}</div>
                        <div>Filtered Requests: ${stats.filtered_requests}</div>
                        <div>Errors: ${stats.errors}</div>
                    `;
                    document.getElementById('analyticsStats').innerHTML = html;
                }
                
                function updateConversationStats(stats) {
                    const html = `
                        <div>Total Conversations: ${stats.total_conversations}</div>
                        <div>Total Messages: ${stats.total_messages}</div>
                        <div>Active Today: ${stats.active_conversations_today}</div>
                        <div>Avg Messages per Conversation: ${stats.average_messages_per_conversation.toFixed(1)}</div>
                    `;
                    document.getElementById('conversationStats').innerHTML = html;
                }
                
                function updateWebhookStats(stats) {
                    const html = `
                        <div>Total Webhooks: ${stats.total_webhooks}</div>
                        <div>Active Webhooks: ${stats.active_webhooks}</div>
                        <div>Total Triggers: ${stats.total_triggers}</div>
                        <div>Success Rate: ${stats.success_rate.toFixed(1)}%</div>
                    `;
                    document.getElementById('webhookStats').innerHTML = html;
                }
                
                async function loadRecentConversations() {
                    try {
                        const response = await fetch('/admin/api/conversations?limit=10', { headers });
                        const conversations = await response.json();
                        
                        if (response.ok) {
                            const html = conversations.map(conv => `
                                <div class="mb-2">
                                    <strong>${conv.conversation_id}</strong> - ${conv.metadata.total_messages} messages
                                    <small class="text-muted">(${new Date(conv.metadata.last_activity).toLocaleString()})</small>
                                </div>
                            `).join('');
                            document.getElementById('recentConversations').innerHTML = html || 'No conversations found';
                        }
                    } catch (error) {
                        console.error('Error loading conversations:', error);
                    }
                }
                
                async function reloadSystemPrompt() {
                    try {
                        const response = await fetch('/admin/api/system/reload-prompt', { 
                            method: 'POST', 
                            headers 
                        });
                        const result = await response.json();
                        
                        if (result.success) {
                            alert('System prompt reloaded successfully');
                        } else {
                            alert('Failed to reload system prompt');
                        }
                    } catch (error) {
                        alert('Error reloading system prompt');
                    }
                }
                
                function exportData() {
                    alert('Export functionality would be implemented here');
                }
                
                // Load stats on page load
                loadStats();
                
                // Auto-refresh every 30 seconds
                setInterval(loadStats, 30000);
            </script>
        </body>
        </html>
        '''
    
    def get_admin_token(self) -> str:
        """Get admin token for initial setup"""
        return self.admin_config.get("admin_token")