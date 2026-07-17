from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_ip = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "conversation_id": self.id,
            "user_ip": self.user_ip,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": {
                "total_messages": len(self.messages),
                "last_activity": self.last_activity.isoformat()
            }
        }

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey('conversations.id'), nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")
    
    def to_dict(self):
        return {
            "message_id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "user_message": self.user_message,
            "bot_response": self.bot_response
        }

class Analytics(Base):
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)  # YYYY-MM-DD format
    total_chats = Column(Integer, default=0)
    unique_users = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    popular_topics = Column(JSON, default=dict)
    daily_stats = Column(JSON, default=dict)
    
    def to_dict(self):
        return {
            "date": self.date,
            "total_chats": self.total_chats,
            "unique_users": self.unique_users,
            "error_count": self.error_count,
            "popular_topics": self.popular_topics or {},
            "daily_stats": self.daily_stats or {}
        }

class Webhook(Base):
    __tablename__ = 'webhooks'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=True)
    url = Column(String, nullable=False)
    events = Column(JSON, nullable=False)  # List of event types
    secret = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "webhook_id": self.id,
            "name": self.name,
            "url": self.url,
            "events": self.events,
            "active": self.active,
            "created_at": self.created_at.isoformat()
        }

class WebhookLog(Base):
    __tablename__ = 'webhook_logs'
    
    id = Column(Integer, primary_key=True)
    webhook_id = Column(String, ForeignKey('webhooks.id'), nullable=False)
    event = Column(String, nullable=False)
    success = Column(Boolean, nullable=False)
    response_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "webhook_id": self.webhook_id,
            "event": self.event,
            "success": self.success,
            "response_code": self.response_code,
            "error_message": self.error_message,
            "timestamp": self.timestamp.isoformat()
        }

class ChatLog(Base):
    __tablename__ = 'chat_logs'
    
    id = Column(Integer, primary_key=True)
    user_ip = Column(String, nullable=False)
    conversation_id = Column(String, nullable=False)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    filtered = Column(Boolean, default=False)
    error_occurred = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            "user_ip": self.user_ip,
            "conversation_id": self.conversation_id,
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "timestamp": self.timestamp.isoformat(),
            "filtered": self.filtered,
            "error_occurred": self.error_occurred
        }

class AdminConfig(Base):
    __tablename__ = 'admin_config'
    
    id = Column(Integer, primary_key=True)
    config_key = Column(String, unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "config_key": self.config_key,
            "config_value": self.config_value,
            "updated_at": self.updated_at.isoformat()
        }