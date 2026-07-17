import os
import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Analytics:
    def __init__(self):
        self.chat_logs_path = "chat_logs"
        self.analytics_file = os.path.join(self.chat_logs_path, "analytics.json")
        self._ensure_directories()
        self.daily_stats = self._load_daily_stats()
    
    def _ensure_directories(self):
        """Ensure analytics directories exist"""
        os.makedirs(self.chat_logs_path, exist_ok=True)
    
    def _load_daily_stats(self) -> Dict[str, Any]:
        """Load daily statistics"""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    data = json.load(f)
                    # Convert unique_users from list back to set
                    if isinstance(data.get("unique_users"), list):
                        data["unique_users"] = set(data["unique_users"])
                    # Convert daily_stats unique_users from list back to set
                    for date, stats in data.get("daily_stats", {}).items():
                        if isinstance(stats.get("unique_users"), list):
                            stats["unique_users"] = set(stats["unique_users"])
                    return data
            else:
                return {
                    "total_chats": 0,
                    "unique_users": set(),
                    "daily_stats": {},
                    "popular_topics": {},
                    "error_count": 0
                }
        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            return {
                "total_chats": 0,
                "unique_users": set(),
                "daily_stats": {},
                "popular_topics": {},
                "error_count": 0
            }
    
    def _save_daily_stats(self):
        """Save daily statistics to file"""
        try:
            # Convert set to list for JSON serialization
            stats_to_save = self.daily_stats.copy()
            stats_to_save["unique_users"] = list(self.daily_stats["unique_users"])
            
            with open(self.analytics_file, 'w') as f:
                json.dump(stats_to_save, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving analytics: {e}")
    
    def log_chat_interaction(self, user_ip: str, user_message: str, bot_response: str):
        """Log a chat interaction"""
        try:
            timestamp = datetime.utcnow().isoformat()
            today = datetime.utcnow().date().isoformat()
            
            # Create detailed log entry
            log_entry = {
                "timestamp": timestamp,
                "user_ip": user_ip,
                "user_message": user_message,
                "bot_response": bot_response,
                "message_length": len(user_message),
                "response_length": len(bot_response)
            }
            
            # Save individual chat log
            chat_log_file = os.path.join(self.chat_logs_path, f"chat_log_{today}.json")
            self._append_to_log_file(chat_log_file, log_entry)
            
            # Update analytics
            self.daily_stats["total_chats"] += 1
            self.daily_stats["unique_users"].add(user_ip)
            
            # Update daily stats
            if today not in self.daily_stats["daily_stats"]:
                self.daily_stats["daily_stats"][today] = {
                    "chats": 0,
                    "unique_users": set()
                }
            
            self.daily_stats["daily_stats"][today]["chats"] += 1
            if isinstance(self.daily_stats["daily_stats"][today]["unique_users"], set):
                self.daily_stats["daily_stats"][today]["unique_users"].add(user_ip)
            else:
                # Convert to set if it's not already
                users = self.daily_stats["daily_stats"][today]["unique_users"]
                if isinstance(users, list):
                    self.daily_stats["daily_stats"][today]["unique_users"] = set(users)
                else:
                    self.daily_stats["daily_stats"][today]["unique_users"] = {str(users)}
                self.daily_stats["daily_stats"][today]["unique_users"].add(user_ip)
            
            # Extract topics (simple keyword extraction)
            self._update_popular_topics(user_message)
            
            # Convert daily stats unique_users set to list for saving
            for date, stats in self.daily_stats["daily_stats"].items():
                if isinstance(stats.get("unique_users"), set):
                    stats["unique_users"] = list(stats["unique_users"])
            
            # Save updated stats
            self._save_daily_stats()
            
        except Exception as e:
            logger.error(f"Error logging chat interaction: {e}")
    
    def _append_to_log_file(self, file_path: str, log_entry: Dict[str, Any]):
        """Append log entry to file"""
        try:
            # Read existing logs
            logs = []
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    logs = json.load(f)
            
            # Append new log
            logs.append(log_entry)
            
            # Write back to file
            with open(file_path, 'w') as f:
                json.dump(logs, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error appending to log file: {e}")
    
    def _update_popular_topics(self, message: str):
        """Update popular topics based on message content"""
        try:
            # Simple keyword extraction
            keywords = ["AI", "poker", "investing", "startup", "technology", "machine learning", 
                       "venture capital", "entrepreneurship", "fintech", "blockchain"]
            
            message_lower = message.lower()
            for keyword in keywords:
                if keyword.lower() in message_lower:
                    if keyword not in self.daily_stats["popular_topics"]:
                        self.daily_stats["popular_topics"][keyword] = 0
                    self.daily_stats["popular_topics"][keyword] += 1
                    
        except Exception as e:
            logger.error(f"Error updating popular topics: {e}")
    
    def log_filtered_request(self, user_ip: str, message: str):
        """Log filtered/blocked request"""
        try:
            timestamp = datetime.utcnow().isoformat()
            
            log_entry = {
                "timestamp": timestamp,
                "user_ip": user_ip,
                "filtered_message": message,
                "reason": "content_filter"
            }
            
            # Save to filtered requests log
            filtered_log_file = os.path.join(self.chat_logs_path, "filtered_requests.json")
            self._append_to_log_file(filtered_log_file, log_entry)
            
        except Exception as e:
            logger.error(f"Error logging filtered request: {e}")
    
    def log_error(self, user_ip: str, error_message: str):
        """Log error occurrence"""
        try:
            timestamp = datetime.utcnow().isoformat()
            
            log_entry = {
                "timestamp": timestamp,
                "user_ip": user_ip,
                "error": error_message
            }
            
            # Save to error log
            error_log_file = os.path.join(self.chat_logs_path, "errors.json")
            self._append_to_log_file(error_log_file, log_entry)
            
            # Update error count
            self.daily_stats["error_count"] += 1
            self._save_daily_stats()
            
        except Exception as e:
            logger.error(f"Error logging error: {e}")
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary"""
        try:
            return {
                "total_chats": self.daily_stats["total_chats"],
                "unique_users": len(self.daily_stats["unique_users"]),
                "popular_topics": self.daily_stats["popular_topics"],
                "error_count": self.daily_stats["error_count"],
                "daily_stats": {
                    date: {
                        "chats": stats["chats"],
                        "unique_users": len(stats["unique_users"])
                    }
                    for date, stats in self.daily_stats["daily_stats"].items()
                }
            }
        except Exception as e:
            logger.error(f"Error getting analytics summary: {e}")
            return {}
    
    def is_healthy(self) -> bool:
        """Check if analytics service is healthy"""
        try:
            return os.path.exists(self.chat_logs_path)
        except:
            return False
