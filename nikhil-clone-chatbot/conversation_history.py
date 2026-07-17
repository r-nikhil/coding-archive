import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid

class ConversationHistory:
    def __init__(self):
        self.history_dir = "conversation_history"
        self._ensure_directories()
        
    def _ensure_directories(self):
        """Ensure conversation history directories exist"""
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
    
    def create_conversation(self, user_ip: str) -> str:
        """Create a new conversation and return conversation ID"""
        conversation_id = str(uuid.uuid4())
        conversation_data = {
            "conversation_id": conversation_id,
            "user_ip": user_ip,
            "created_at": datetime.now().isoformat(),
            "messages": [],
            "metadata": {
                "total_messages": 0,
                "last_activity": datetime.now().isoformat()
            }
        }
        
        file_path = os.path.join(self.history_dir, f"{conversation_id}.json")
        with open(file_path, 'w') as f:
            json.dump(conversation_data, f, indent=2)
        
        return conversation_id
    
    def add_message(self, conversation_id: str, user_message: str, bot_response: str, timestamp: str = None):
        """Add a message exchange to conversation history"""
        if not timestamp:
            timestamp = datetime.now().isoformat()
        
        file_path = os.path.join(self.history_dir, f"{conversation_id}.json")
        
        try:
            # Load existing conversation
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    conversation_data = json.load(f)
            else:
                # Create new conversation if it doesn't exist
                conversation_data = {
                    "conversation_id": conversation_id,
                    "user_ip": "unknown",
                    "created_at": timestamp,
                    "messages": [],
                    "metadata": {
                        "total_messages": 0,
                        "last_activity": timestamp
                    }
                }
            
            # Add new message
            message_entry = {
                "timestamp": timestamp,
                "user_message": user_message,
                "bot_response": bot_response,
                "message_id": str(uuid.uuid4())
            }
            
            conversation_data["messages"].append(message_entry)
            conversation_data["metadata"]["total_messages"] += 1
            conversation_data["metadata"]["last_activity"] = timestamp
            
            # Save updated conversation
            with open(file_path, 'w') as f:
                json.dump(conversation_data, f, indent=2)
                
        except Exception as e:
            print(f"Error adding message to conversation {conversation_id}: {e}")
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation history by ID"""
        file_path = os.path.join(self.history_dir, f"{conversation_id}.json")
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading conversation {conversation_id}: {e}")
            return None
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations"""
        conversations = []
        
        try:
            for filename in os.listdir(self.history_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.history_dir, filename)
                    with open(file_path, 'r') as f:
                        conversation = json.load(f)
                        conversations.append(conversation)
            
            # Sort by last activity
            conversations.sort(key=lambda x: x["metadata"]["last_activity"], reverse=True)
            return conversations[:limit]
            
        except Exception as e:
            print(f"Error getting recent conversations: {e}")
            return []
    
    def get_conversation_context(self, conversation_id: str, last_n_messages: int = 5) -> str:
        """Get conversation context for RAG"""
        conversation = self.get_conversation(conversation_id)
        
        if not conversation:
            return ""
        
        messages = conversation.get("messages", [])
        recent_messages = messages[-last_n_messages:] if len(messages) > last_n_messages else messages
        
        context = "Previous conversation context:\n"
        for msg in recent_messages:
            context += f"User: {msg['user_message']}\n"
            context += f"Assistant: {msg['bot_response']}\n\n"
        
        return context
    
    def cleanup_old_conversations(self, days_old: int = 30):
        """Clean up conversations older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        try:
            for filename in os.listdir(self.history_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.history_dir, filename)
                    with open(file_path, 'r') as f:
                        conversation = json.load(f)
                    
                    created_at = datetime.fromisoformat(conversation["created_at"])
                    if created_at < cutoff_date:
                        os.remove(file_path)
                        print(f"Deleted old conversation: {filename}")
                        
        except Exception as e:
            print(f"Error cleaning up old conversations: {e}")
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        stats = {
            "total_conversations": 0,
            "total_messages": 0,
            "active_conversations_today": 0,
            "average_messages_per_conversation": 0
        }
        
        try:
            today = datetime.now().date()
            
            for filename in os.listdir(self.history_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.history_dir, filename)
                    with open(file_path, 'r') as f:
                        conversation = json.load(f)
                    
                    stats["total_conversations"] += 1
                    stats["total_messages"] += conversation["metadata"]["total_messages"]
                    
                    # Check if active today
                    last_activity = datetime.fromisoformat(conversation["metadata"]["last_activity"]).date()
                    if last_activity == today:
                        stats["active_conversations_today"] += 1
            
            if stats["total_conversations"] > 0:
                stats["average_messages_per_conversation"] = stats["total_messages"] / stats["total_conversations"]
            
        except Exception as e:
            print(f"Error getting conversation stats: {e}")
        
        return stats
    
    def is_healthy(self) -> bool:
        """Check if conversation history service is healthy"""
        return os.path.exists(self.history_dir) and os.path.isdir(self.history_dir)