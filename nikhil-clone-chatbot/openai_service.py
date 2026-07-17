import os
import logging
from openai import OpenAI
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.system_prompt = self._load_system_prompt()
        self.max_tokens = 300  # Limit response length
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from file"""
        try:
            with open("system_prompt.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning("System prompt file not found, using default")
            return self._get_default_system_prompt()
        except Exception as e:
            logger.error(f"Error loading system prompt: {e}")
            return self._get_default_system_prompt()
    
    def _get_default_system_prompt(self) -> str:
        """Default system prompt if file is not found"""
        return """You are Nikhil, an AI resident at Accel and poker professional. Use the retrieved blog content to answer questions about AI, investing, poker, and any relevant projects I have written. Keep responses conversational and helpful. Limit your responses to around 200 words."""
    
    def generate_response(self, user_message: str, relevant_content: List[Dict[str, Any]], conversation_context: str = "") -> str:
        """Generate response using OpenAI GPT-4o with RAG context"""
        try:
            # Prepare context from relevant content
            context = self._prepare_context(relevant_content)
            
            # Prepare messages
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self._format_user_message(user_message, context, conversation_context)}
            ]
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            response_text = response.choices[0].message.content
            
            # Log token usage
            self._log_token_usage(response.usage)
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later or email contact@rnikhil.com for direct assistance."
    
    def _prepare_context(self, relevant_content: List[Dict[str, Any]]) -> str:
        """Prepare context string from relevant content"""
        if not relevant_content:
            return "No relevant blog content found."
        
        context_parts = []
        for item in relevant_content:
            metadata = item.get("metadata", {})
            content = item.get("content", "")
            
            # Format each piece of content
            title = metadata.get("title", "Untitled")
            date = metadata.get("date", "")
            
            context_part = f"Title: {title}\n"
            if date:
                context_part += f"Date: {date}\n"
            context_part += f"Content: {content[:500]}...\n\n"  # Limit content length
            
            context_parts.append(context_part)
        
        return "Relevant blog content:\n\n" + "\n".join(context_parts)
    
    def _format_user_message(self, user_message: str, context: str, conversation_context: str = "") -> str:
        """Format user message with context and conversation history"""
        message_parts = []
        
        if conversation_context:
            message_parts.append(f"Conversation history:\n{conversation_context}")
        
        message_parts.append(f"User question: {user_message}")
        
        if context:
            message_parts.append(context)
        
        message_parts.append("Please answer the user's question based on the relevant blog content provided above. If the content doesn't contain relevant information, you can provide a general helpful response based on your knowledge as Nikhil.")
        
        return "\n\n".join(message_parts)
    
    def _log_token_usage(self, usage):
        """Log token usage for monitoring"""
        try:
            logger.info(f"Token usage - Prompt: {usage.prompt_tokens}, Completion: {usage.completion_tokens}, Total: {usage.total_tokens}")
        except Exception as e:
            logger.error(f"Error logging token usage: {e}")
    
    def is_healthy(self) -> bool:
        """Check if OpenAI service is healthy"""
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=1
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False
    
    def reload_system_prompt(self):
        """Reload system prompt from file"""
        self.system_prompt = self._load_system_prompt()
        logger.info("System prompt reloaded")
