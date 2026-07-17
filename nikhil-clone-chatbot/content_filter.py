import re
import logging
from typing import List

logger = logging.getLogger(__name__)

class ContentFilter:
    def __init__(self):
        # Basic inappropriate content patterns
        self.nsfw_patterns = [
            r'\b(sex|sexual|porn|explicit|nude|naked)\b',
            r'\b(fuck|shit|damn|hell|bitch|ass|bastard)\b',
            r'\b(kill|murder|suicide|death|die)\b',
            r'\b(drug|cocaine|marijuana|weed|heroin)\b',
            r'\b(hate|racism|nazi|terrorist)\b'
        ]
        
        # Prompt injection patterns
        self.injection_patterns = [
            r'ignore\s+previous\s+instructions',
            r'system\s*:\s*',
            r'assistant\s*:\s*',
            r'user\s*:\s*',
            r'<\s*system\s*>',
            r'<\s*assistant\s*>',
            r'<\s*user\s*>',
            r'pretend\s+to\s+be',
            r'act\s+as\s+if',
            r'roleplay\s+as',
            r'simulate\s+being',
            r'forget\s+everything',
            r'new\s+instructions',
            r'override\s+your',
            r'jailbreak',
            r'developer\s+mode'
        ]
        
        # Compile patterns for efficiency
        self.compiled_nsfw = [re.compile(pattern, re.IGNORECASE) for pattern in self.nsfw_patterns]
        self.compiled_injection = [re.compile(pattern, re.IGNORECASE) for pattern in self.injection_patterns]
    
    def is_safe(self, text: str) -> bool:
        """Check if text is safe (not inappropriate or injection attempt)"""
        try:
            # Check for NSFW content
            if self._contains_nsfw(text):
                logger.warning(f"NSFW content detected: {text[:50]}...")
                return False
            
            # Check for prompt injection attempts
            if self._contains_injection(text):
                logger.warning(f"Prompt injection detected: {text[:50]}...")
                return False
            
            # Check for excessive length (potential spam)
            if len(text) > 1000:
                logger.warning(f"Message too long: {len(text)} characters")
                return False
            
            # Check for repeated characters (potential spam)
            if self._is_spam(text):
                logger.warning(f"Spam detected: {text[:50]}...")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in content filtering: {e}")
            # Default to safe if filter fails
            return True
    
    def _contains_nsfw(self, text: str) -> bool:
        """Check if text contains NSFW content"""
        for pattern in self.compiled_nsfw:
            if pattern.search(text):
                return True
        return False
    
    def _contains_injection(self, text: str) -> bool:
        """Check if text contains prompt injection attempts"""
        for pattern in self.compiled_injection:
            if pattern.search(text):
                return True
        return False
    
    def _is_spam(self, text: str) -> bool:
        """Check if text appears to be spam"""
        # Check for repeated characters
        if len(set(text)) < len(text) * 0.1:  # Less than 10% unique characters
            return True
        
        # Check for repeated words
        words = text.split()
        if len(words) > 5:
            unique_words = set(words)
            if len(unique_words) < len(words) * 0.5:  # Less than 50% unique words
                return True
        
        # Check for excessive punctuation
        punct_count = sum(1 for char in text if char in '!@#$%^&*()_+[]{}|;:,.<>?')
        if punct_count > len(text) * 0.3:  # More than 30% punctuation
            return True
        
        return False
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize input text"""
        try:
            # Remove excessive whitespace
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Remove potential HTML/XML tags
            text = re.sub(r'<[^>]+>', '', text)
            
            # Remove potential script tags
            text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
            
            # Limit length
            if len(text) > 1000:
                text = text[:1000]
            
            return text
            
        except Exception as e:
            logger.error(f"Error sanitizing input: {e}")
            return text
    
    def get_violation_reason(self, text: str) -> str:
        """Get specific reason for content violation"""
        try:
            if self._contains_nsfw(text):
                return "inappropriate_content"
            elif self._contains_injection(text):
                return "prompt_injection"
            elif len(text) > 1000:
                return "message_too_long"
            elif self._is_spam(text):
                return "spam_detected"
            else:
                return "safe"
        except Exception as e:
            logger.error(f"Error getting violation reason: {e}")
            return "unknown"
