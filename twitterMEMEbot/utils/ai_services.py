import os
import requests
from typing import Optional
import anthropic
import openai
import logging

class AIServices:
    def __init__(self):
        self.anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        
        # Validate API keys
        if not self.anthropic_key:
            logging.error("Missing ANTHROPIC_API_KEY")
            raise ValueError("ANTHROPIC_API_KEY is required")
        if not self.openai_key:
            logging.error("Missing OPENAI_API_KEY")
            raise ValueError("OPENAI_API_KEY is required")
            
        try:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
            openai.api_key = self.openai_key
            logging.info("Successfully initialized AI clients")
        except Exception as e:
            logging.error(f"Failed to initialize AI clients: {str(e)}")
            raise
            
        logging.info("Successfully initialized AI services")

    def summarize_tweet(self, tweet_text: str, max_length: int = 300) -> str:
        """
        Use Claude to summarize tweet text while maintaining its tone and key details
        """
        if len(tweet_text) <= max_length:
            return tweet_text
            
        try:
            prompt = f"""
            Please summarize the following tweet while maintaining its key details, humor, and style.
            Keep the most interesting and engaging parts. The summary MUST be under {max_length} characters:

            Tweet: {tweet_text}

            Important: Keep the summary concise and impactful for meme generation.
            """
            
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0.7,
                system="You are an expert at summarizing tweets while maintaining their original tone, humor, and key details. Your summaries are perfect for meme generation.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            summary = response.content[0].text.strip()
            
            # Ensure we don't exceed max length
            if len(summary) > max_length:
                logging.warning(f"Summary still too long ({len(summary)} chars), truncating...")
                summary = summary[:max_length-3] + "..."
                
            logging.info(f"Successfully summarized tweet from {len(tweet_text)} to {len(summary)} chars")
            return summary
            
        except Exception as e:
            logging.error(f"Error summarizing tweet: {str(e)}")
            # Fallback: truncate original text with ellipsis
            return tweet_text[:max_length-3] + "..."

    def generate_meme(self, text: str) -> Optional[str]:
        """
        Generate a meme using OpenAI's DALL-E model
        Returns the URL of the generated image
        """
        if not text:
            logging.error("Cannot generate meme: Empty text provided")
            return None
            
        # Ensure text is within limits
        if len(text) > 300:
            text = self.summarize_tweet(text)
            
        try:
            # Create a meme-specific prompt
            prompt = f"""Create a funny meme image for this text: '{text}'
            Make it visually engaging and humorous, suitable for social media.
            The image should be clear and easily readable when shared on Twitter."""
            
            logging.info(f"Generating DALL-E image for text: {text[:50]}...")
            
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            if not response or not response.data:
                logging.error("No image generated in DALL-E response")
                return None
                
            image_url = response.data[0].url
            logging.info(f"Successfully generated image: {image_url}")
            return image_url
            
        except openai.RateLimitError:
            logging.error("OpenAI rate limit exceeded - please wait before retrying")
            return None
        except openai.AuthenticationError:
            logging.error("Invalid OpenAI API key - please verify API key")
            return None
        except Exception as e:
            logging.error(f"Unexpected error generating image: {str(e)}")
            return None
