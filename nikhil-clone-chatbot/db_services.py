from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from models import Conversation, Message, Analytics, Webhook, WebhookLog, ChatLog, AdminConfig
from database import db_manager
import json
import logging

logger = logging.getLogger(__name__)

class DatabaseConversationService:
    """Database-backed conversation history service"""
    
    def create_conversation(self, user_ip: str) -> str:
        """Create a new conversation and return conversation ID"""
        with db_manager.get_session() as session:
            conversation = Conversation(user_ip=user_ip)
            session.add(conversation)
            session.commit()
            logger.info(f"Created new conversation: {conversation.id}")
            return conversation.id
    
    def add_message(self, conversation_id: str, user_message: str, bot_response: str, timestamp: str = None):
        """Add a message exchange to conversation history"""
        with db_manager.get_session() as session:
            # Get or create conversation
            conversation = session.query(Conversation).filter_by(id=conversation_id).first()
            if not conversation:
                # Create conversation if it doesn't exist
                conversation = Conversation(id=conversation_id, user_ip="unknown")
                session.add(conversation)
            
            # Add message
            message = Message(
                conversation_id=conversation_id,
                user_message=user_message,
                bot_response=bot_response,
                timestamp=datetime.fromisoformat(timestamp.replace('Z', '+00:00')) if timestamp else datetime.utcnow()
            )
            session.add(message)
            
            # Update conversation last activity
            conversation.last_activity = datetime.utcnow()
            session.commit()
            logger.info(f"Added message to conversation: {conversation_id}")
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation history by ID"""
        with db_manager.get_session() as session:
            conversation = session.query(Conversation).filter_by(id=conversation_id).first()
            if conversation:
                return conversation.to_dict()
            return None
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations"""
        with db_manager.get_session() as session:
            conversations = session.query(Conversation)\
                .order_by(desc(Conversation.last_activity))\
                .limit(limit)\
                .all()
            return [conv.to_dict() for conv in conversations]
    
    def get_conversation_context(self, conversation_id: str, last_n_messages: int = 5) -> str:
        """Get conversation context for RAG"""
        with db_manager.get_session() as session:
            messages = session.query(Message)\
                .filter_by(conversation_id=conversation_id)\
                .order_by(desc(Message.timestamp))\
                .limit(last_n_messages)\
                .all()
            
            if not messages:
                return ""
            
            # Build context string
            context_parts = []
            for msg in reversed(messages):  # Reverse to get chronological order
                context_parts.append(f"User: {msg.user_message}")
                context_parts.append(f"Nikhil: {msg.bot_response}")
            
            return "\n".join(context_parts)
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        with db_manager.get_session() as session:
            total_conversations = session.query(Conversation).count()
            total_messages = session.query(Message).count()
            
            # Get recent activity (last 24 hours)
            yesterday = datetime.utcnow() - timedelta(days=1)
            recent_conversations = session.query(Conversation)\
                .filter(Conversation.last_activity >= yesterday).count()
            
            return {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "recent_conversations_24h": recent_conversations,
                "average_messages_per_conversation": total_messages / max(total_conversations, 1)
            }
    
    def cleanup_old_conversations(self, days_old: int = 30):
        """Clean up conversations older than specified days"""
        with db_manager.get_session() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            old_conversations = session.query(Conversation)\
                .filter(Conversation.last_activity < cutoff_date).all()
            
            count = len(old_conversations)
            for conversation in old_conversations:
                session.delete(conversation)
            
            session.commit()
            logger.info(f"Cleaned up {count} old conversations")
            return count
    
    def is_healthy(self) -> bool:
        """Check if conversation service is healthy"""
        return db_manager.health_check()

class DatabaseAnalyticsService:
    """Database-backed analytics service"""
    
    def log_chat_interaction(self, user_ip: str, conversation_id: str, user_message: str, bot_response: str):
        """Log a chat interaction"""
        with db_manager.get_session() as session:
            # Log individual chat
            chat_log = ChatLog(
                user_ip=user_ip,
                conversation_id=conversation_id,
                user_message=user_message,
                bot_response=bot_response
            )
            session.add(chat_log)
            
            # Update daily analytics
            today = datetime.utcnow().strftime('%Y-%m-%d')
            analytics = session.query(Analytics).filter_by(date=today).first()
            
            if not analytics:
                analytics = Analytics(date=today, total_chats=0, unique_users=0, error_count=0)
                session.add(analytics)
            
            analytics.total_chats = (analytics.total_chats or 0) + 1
            
            # Update popular topics
            topics = analytics.popular_topics or {}
            self._update_popular_topics(topics, user_message)
            analytics.popular_topics = topics
            
            session.commit()
    
    def _update_popular_topics(self, topics: Dict[str, int], message: str):
        """Update popular topics based on message content"""
        keywords = ['AI', 'investing', 'poker', 'Accel', 'startup', 'technology', 'finance', 'strategy']
        message_lower = message.lower()
        
        for keyword in keywords:
            if keyword.lower() in message_lower:
                topics[keyword] = topics.get(keyword, 0) + 1
    
    def log_filtered_request(self, user_ip: str, message: str):
        """Log filtered/blocked request"""
        with db_manager.get_session() as session:
            chat_log = ChatLog(
                user_ip=user_ip,
                conversation_id="filtered",
                user_message=message,
                bot_response="[FILTERED]",
                filtered=True
            )
            session.add(chat_log)
            session.commit()
    
    def log_error(self, user_ip: str, error_message: str):
        """Log error occurrence"""
        with db_manager.get_session() as session:
            chat_log = ChatLog(
                user_ip=user_ip,
                conversation_id="error",
                user_message="[ERROR]",
                bot_response=error_message,
                error_occurred=True
            )
            session.add(chat_log)
            
            # Update daily error count
            today = datetime.utcnow().strftime('%Y-%m-%d')
            analytics = session.query(Analytics).filter_by(date=today).first()
            
            if not analytics:
                analytics = Analytics(date=today, total_chats=0, unique_users=0, error_count=0)
                session.add(analytics)
            
            analytics.error_count = (analytics.error_count or 0) + 1
            session.commit()
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary"""
        with db_manager.get_session() as session:
            # Get total stats
            total_chats = session.query(ChatLog).filter(ChatLog.filtered == False).count()
            unique_users = session.query(func.count(func.distinct(ChatLog.user_ip))).scalar()
            error_count = session.query(ChatLog).filter(ChatLog.error_occurred == True).count()
            
            # Get daily stats (last 7 days)
            daily_stats = {}
            for i in range(7):
                date = (datetime.utcnow() - timedelta(days=i)).strftime('%Y-%m-%d')
                analytics = session.query(Analytics).filter_by(date=date).first()
                if analytics:
                    daily_stats[date] = {
                        "chats": analytics.total_chats,
                        "unique_users": analytics.unique_users or 0
                    }
            
            # Get popular topics
            popular_topics = {}
            recent_analytics = session.query(Analytics)\
                .order_by(desc(Analytics.date))\
                .limit(7)\
                .all()
            
            for analytics in recent_analytics:
                if analytics.popular_topics:
                    for topic, count in analytics.popular_topics.items():
                        popular_topics[topic] = popular_topics.get(topic, 0) + count
            
            return {
                "total_chats": total_chats,
                "unique_users": unique_users or 0,
                "error_count": error_count,
                "daily_stats": daily_stats,
                "popular_topics": popular_topics
            }
    
    def is_healthy(self) -> bool:
        """Check if analytics service is healthy"""
        return db_manager.health_check()

class DatabaseWebhookService:
    """Database-backed webhook service"""
    
    def add_webhook(self, url: str, events: List[str], secret: str = None, name: str = None) -> str:
        """Add a new webhook"""
        with db_manager.get_session() as session:
            webhook = Webhook(
                name=name,
                url=url,
                events=events,
                secret=secret
            )
            session.add(webhook)
            session.commit()
            logger.info(f"Added webhook: {webhook.id}")
            return webhook.id
    
    def get_active_webhooks(self) -> List[Dict[str, Any]]:
        """Get all active webhooks"""
        with db_manager.get_session() as session:
            webhooks = session.query(Webhook).filter_by(active=True).all()
            return [webhook.to_dict() for webhook in webhooks]
    
    def toggle_webhook(self, webhook_id: str, active: bool) -> bool:
        """Enable/disable a webhook"""
        with db_manager.get_session() as session:
            webhook = session.query(Webhook).filter_by(id=webhook_id).first()
            if webhook:
                webhook.active = active
                session.commit()
                return True
            return False
    
    def log_webhook_event(self, webhook_id: str, event: str, success: bool, response_code: int = None, error: str = None):
        """Log webhook event"""
        with db_manager.get_session() as session:
            webhook_log = WebhookLog(
                webhook_id=webhook_id,
                event=event,
                success=success,
                response_code=response_code,
                error_message=error
            )
            session.add(webhook_log)
            session.commit()
    
    def get_webhook_stats(self) -> Dict[str, Any]:
        """Get webhook statistics"""
        with db_manager.get_session() as session:
            total_webhooks = session.query(Webhook).count()
            active_webhooks = session.query(Webhook).filter_by(active=True).count()
            
            # Get recent webhook activity
            yesterday = datetime.utcnow() - timedelta(days=1)
            recent_events = session.query(WebhookLog)\
                .filter(WebhookLog.timestamp >= yesterday).count()
            
            successful_events = session.query(WebhookLog)\
                .filter(and_(WebhookLog.timestamp >= yesterday, WebhookLog.success == True)).count()
            
            return {
                "total_webhooks": total_webhooks,
                "active_webhooks": active_webhooks,
                "recent_events_24h": recent_events,
                "success_rate_24h": (successful_events / max(recent_events, 1)) * 100
            }
    
    def is_healthy(self) -> bool:
        """Check if webhook service is healthy"""
        return db_manager.health_check()

class DatabaseAdminService:
    """Database-backed admin configuration service"""
    
    def get_config(self, key: str) -> Optional[str]:
        """Get configuration value"""
        with db_manager.get_session() as session:
            config = session.query(AdminConfig).filter_by(config_key=key).first()
            return config.config_value if config else None
    
    def set_config(self, key: str, value: str):
        """Set configuration value"""
        with db_manager.get_session() as session:
            config = session.query(AdminConfig).filter_by(config_key=key).first()
            if config:
                config.config_value = value
                config.updated_at = datetime.utcnow()
            else:
                config = AdminConfig(config_key=key, config_value=value)
                session.add(config)
            session.commit()
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values"""
        with db_manager.get_session() as session:
            configs = session.query(AdminConfig).all()
            return {config.config_key: config.config_value for config in configs}
    
    def is_healthy(self) -> bool:
        """Check if admin service is healthy"""
        return db_manager.health_check()

# Global service instances
db_conversation_service = DatabaseConversationService()
db_analytics_service = DatabaseAnalyticsService()
db_webhook_service = DatabaseWebhookService()
db_admin_service = DatabaseAdminService()