# Nikhil's AI Chatbot API Documentation

**Version:** 1.0.0  
**Base URL:** `https://llm-chat-backend-NikhilR24.replit.app`  
**Status:** Production Ready

## Overview

Comprehensive Flask backend for an AI-powered chatbot that combines Retrieval-Augmented Generation (RAG) with OpenAI's GPT-4o to deliver personalized responses about AI, investing, poker, and other topics based on blog content.

### Core Features
- 🤖 RAG with ChromaDB embeddings
- 💬 Conversation history management  
- 🔔 Real-time webhook notifications
- 🛡️ Content filtering & rate limiting
- 📊 Advanced analytics dashboard
- ⚙️ Web-based admin panel

### Technical Stack
- Flask with CORS support
- OpenAI GPT-4o & text-embedding-ada-002
- ChromaDB vector database
- Bootstrap admin interface

---

## Authentication

Most endpoints are public. Admin panel requires token-based authentication.

**Admin Login:**
```http
POST /admin/login
Content-Type: application/json

{
  "token": "your-admin-token"
}
```

**Admin requests require header:**
```
Authorization: Bearer your-admin-token
```

---

## Core Chat API

### Get API Information
```http
GET /
```
Returns API overview, available endpoints, and features.

**Response:**
```json
{
  "message": "Nikhil's AI-Powered Chatbot Backend",
  "description": "Flask backend with RAG capabilities...",
  "api_endpoints": {
    "chat": "POST /api/chat - Main chat interface",
    "health": "GET /api/health - System health check"
  },
  "features": [...],
  "version": "1.0.0",
  "status": "operational"
}
```

### Health Check
```http
GET /api/health
```
Monitor system health and service status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-08T09:19:32.123456",
  "services": {
    "rag": true,
    "openai": true,
    "analytics": true,
    "conversation_history": true,
    "webhook_service": true
  }
}
```

### Chat Interface
```http
POST /api/chat
Content-Type: application/json
```

Main chat endpoint with conversation history support.

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | User's chat message (max 1000 chars) |
| conversation_id | string | No | Existing conversation ID (auto-generated if not provided) |
| timestamp | string | No | ISO 8601 timestamp (auto-generated if not provided) |

**Request Example:**
```json
{
  "message": "Tell me about your experience with AI and investing",
  "conversation_id": "optional-existing-id",
  "timestamp": "2025-07-08T09:20:00Z"
}
```

**Response:**
```json
{
  "response": "Based on my experience at Accel as an AI resident...",
  "timestamp": "2025-07-08T09:20:01.234567",
  "conversation_id": "abc123-def456-ghi789"
}
```

**Rate Limits:**
- 10 requests per minute per IP
- 10 chats per user session

---

## Conversation Management

### Get Specific Conversation
```http
GET /api/conversation/{conversation_id}
```
Retrieve complete conversation history by ID.

**Response:**
```json
{
  "conversation_id": "abc123-def456-ghi789",
  "user_ip": "127.0.0.1", 
  "created_at": "2025-07-08T09:16:35.199715",
  "messages": [
    {
      "timestamp": "2025-07-08T09:16:35Z",
      "user_message": "Tell me about your poker background",
      "bot_response": "I played poker professionally from 2018 to 2021...",
      "message_id": "msg-001"
    }
  ],
  "metadata": {
    "total_messages": 1,
    "last_activity": "2025-07-08T09:16:35Z"
  }
}
```

### Get Recent Conversations
```http
GET /api/conversations/recent?limit=10
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | integer | 10 | Number of conversations to return |

---

## Analytics

### Analytics Summary
```http
GET /api/analytics/summary
```

Get comprehensive analytics data.

**Response:**
```json
{
  "total_chats": 6,
  "unique_users": 2,
  "error_count": 0,
  "daily_stats": {
    "2025-07-08": {
      "chats": 6,
      "unique_users": 2
    }
  },
  "popular_topics": {
    "AI": 4,
    "poker": 3,
    "investing": 2
  }
}
```

---

## Admin Panel

Web-based administration interface with authentication.

### Admin Endpoints
- `GET /admin/login` - Bootstrap-styled login interface
- `GET /admin/dashboard` - Real-time system monitoring dashboard (requires auth)
- `GET /admin/api/stats` - Detailed system statistics (requires auth)
- `POST /admin/api/system/reload-prompt` - Reload system prompt from file (requires auth)

---

## Webhooks

Real-time event notifications for integrations.

### Supported Events
| Event | Description | Payload |
|-------|-------------|---------|
| new_message | New chat message received | conversation_id, user_ip, message, response, timestamp |
| message_filtered | Message blocked by content filter | user_ip, message, reason |
| error | System error occurred | error, user_ip, timestamp |

### Configure Webhooks
```http
POST /admin/api/webhooks
Authorization: Bearer your-admin-token
Content-Type: application/json

{
  "url": "https://your-app.com/webhook",
  "events": ["new_message", "error"],
  "secret": "optional-hmac-secret",
  "name": "My Integration"
}
```

### Webhook Payload Example
```json
{
  "event": "new_message",
  "timestamp": "2025-07-08T09:20:00Z",
  "data": {
    "conversation_id": "abc123-def456",
    "user_ip": "127.0.0.1",
    "message": "Hello!",
    "response": "Hi there! How can I help you?",
    "timestamp": "2025-07-08T09:20:00Z"
  }
}
```

---

## Usage Examples

### JavaScript/Frontend Integration
```javascript
// Simple chat implementation
async function sendMessage(message, conversationId = null) {
  const response = await fetch('https://llm-chat-backend-NikhilR24.replit.app/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      conversation_id: conversationId,
      timestamp: new Date().toISOString()
    })
  });
  
  const data = await response.json();
  return data;
}

// Usage
sendMessage("Tell me about AI in investing")
  .then(response => {
    console.log('Bot response:', response.response);
    console.log('Conversation ID:', response.conversation_id);
  });
```

### Python Integration
```python
import requests
from datetime import datetime

def chat_with_nikhil(message, conversation_id=None):
    url = "https://llm-chat-backend-NikhilR24.replit.app/api/chat"
    payload = {
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    
    if conversation_id:
        payload["conversation_id"] = conversation_id
    
    response = requests.post(url, json=payload)
    return response.json()

# Usage
result = chat_with_nikhil("What's your poker background?")
print(f"Response: {result['response']}")
print(f"Conversation ID: {result['conversation_id']}")
```

### cURL Examples
```bash
# Health check
curl https://llm-chat-backend-NikhilR24.replit.app/api/health

# Send chat message
curl -X POST https://llm-chat-backend-NikhilR24.replit.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tell me about your AI experience at Accel",
    "timestamp": "2025-07-08T12:00:00Z"
  }'

# Get analytics
curl https://llm-chat-backend-NikhilR24.replit.app/api/analytics/summary
```

---

## Error Handling

### HTTP Status Codes
| Code | Description | Common Causes |
|------|-------------|---------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Missing message, empty input, message too long |
| 401 | Unauthorized | Invalid admin token |
| 404 | Not Found | Conversation ID doesn't exist |
| 429 | Rate Limited | Too many requests or daily chat limit reached |
| 500 | Internal Error | Server error, OpenAI API issues |

### Error Response Format
```json
{
  "error": "Message contains inappropriate content"
}
```

---

## Support

For technical support or questions:
- Check the [health endpoint](https://llm-chat-backend-NikhilR24.replit.app/api/health) for system status
- Review the admin panel for detailed monitoring  
- Contact: contact@rnikhil.com