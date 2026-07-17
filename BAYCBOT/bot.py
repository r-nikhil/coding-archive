import os
import time
import logging
import threading
import json
from datetime import datetime
import requests
import tweepy
from models import Interaction, BotMetrics
from database import db
from api_clients import OpenAIClient, ReplicateClient
from queue_manager import init_queue

logger = logging.getLogger(__name__)

class RateLimitTracker:
    """Centralized rate limit tracking for Twitter API endpoints"""
    def __init__(self):
        self._limits = {}
        self._reset_times = {}
        self._lock = threading.Lock()
        self._base_delay = 2100  # 35 minutes base delay
        self._minimum_wait_time = 300  # 5 minutes minimum wait
        self._max_retries = 3
        self._attempt_counts = {}
        self._last_request_times = {}
        logger.info("RateLimitTracker initialized with 35 minute base delay and 5 minute minimum wait")
        
    def update_limits(self, endpoint, headers):
        """Update rate limit information from response headers"""
        with self._lock:
            if 'x-rate-limit-remaining' in headers:
                remaining = int(headers['x-rate-limit-remaining'])
                self._limits[endpoint] = remaining
                logger.info(f"Rate limit remaining for {endpoint}: {remaining}")
            if 'x-rate-limit-reset' in headers:
                reset_time = int(headers['x-rate-limit-reset'])
                self._reset_times[endpoint] = reset_time
                wait_time = max(0, reset_time - int(time.time()))
                logger.info(f"Rate limit reset time for {endpoint}: {wait_time} seconds remaining")
                
    def check_rate_limit(self, endpoint):
        """Check if we can make a request to the endpoint with conservative rate limiting"""
        with self._lock:
            # Initialize tracking data if not exists
            if endpoint not in self._attempt_counts:
                self._attempt_counts[endpoint] = 0
            if endpoint not in self._last_request_times:
                self._last_request_times[endpoint] = 0
            
            current_time = int(time.time())
            
            # Always enforce minimum wait time between requests
            last_request_time = self._last_request_times.get(endpoint, 0)
            time_since_last_request = current_time - last_request_time
            
            if time_since_last_request < self._minimum_wait_time:
                wait_needed = self._minimum_wait_time - time_since_last_request
                logger.info(f"Enforcing minimum wait time for {endpoint}. Need to wait {wait_needed} seconds")
                return False
            
            # Check if endpoint is being tracked
            if endpoint not in self._limits:
                logger.info(f"No rate limit information for {endpoint}, initializing tracking with conservative limits")
                self._limits[endpoint] = 250  # More conservative initial limit
                self._last_request_times[endpoint] = current_time
                return True
                
            # Check remaining calls with more conservative buffer
            if self._limits[endpoint] <= 10:  # Increased conservative buffer
                reset_time = self._reset_times.get(endpoint, current_time + self._base_delay)
                if reset_time > current_time:
                    wait_time = reset_time - current_time
                    self._attempt_counts[endpoint] += 1
                    # More conservative backoff calculation
                    backoff_time = min(self._base_delay * (3 ** self._attempt_counts[endpoint]), 14400)  # Max 4 hours
                    total_wait = max(wait_time + backoff_time, self._minimum_wait_time)
                    
                    logger.warning(
                        f"Rate limit protection activated for {endpoint}:\n"
                        f"- Remaining calls: {self._limits[endpoint]}\n"
                        f"- Base wait time: {wait_time}s\n"
                        f"- Backoff time: {backoff_time}s\n"
                        f"- Total wait: {total_wait}s\n"
                        f"- Attempt count: {self._attempt_counts[endpoint]}\n"
                        f"- Time since last request: {current_time - self._last_request_times.get(endpoint, 0)}s"
                    )
                    return False
            else:
                # Update last request time and reset attempt count on successful check
                self._last_request_times[endpoint] = current_time
                if self._attempt_counts[endpoint] > 0:
                    logger.info(f"Resetting attempt count for {endpoint} after successful rate limit check")
                self._attempt_counts[endpoint] = 0
                
            return True
            
    def get_wait_time(self, endpoint):
        """Get the time to wait before next request with exponential backoff"""
        with self._lock:
            current_time = int(time.time())
            reset_time = self._reset_times.get(endpoint, current_time + self._base_delay)
            base_wait = max(0, reset_time - current_time)
            
            # Add exponential backoff based on attempt count
            attempt_count = self._attempt_counts.get(endpoint, 0)
            backoff_time = min(self._base_delay * (2 ** attempt_count), 7200) if attempt_count > 0 else 0
            
            total_wait = base_wait + backoff_time
            logger.info(
                f"Calculated wait time for {endpoint}: "
                f"Base wait: {base_wait}s, "
                f"Backoff: {backoff_time}s, "
                f"Total: {total_wait}s"
            )
            return total_wait

# Global rate limit tracker instance
rate_limit_tracker = RateLimitTracker()

class TwitterAPIError(Exception):
    """Custom exception for Twitter API errors"""
    pass

class TwitterBot:
    def __init__(self):
        try:
            # Initialize with bearer token first
            self.twitter_client = tweepy.Client(
                bearer_token=os.environ.get('TWITTER_BEARER_TOKEN'),
                consumer_key=os.environ.get('TWITTER_API_KEY'),
                consumer_secret=os.environ.get('TWITTER_API_SECRET'),
                access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            
            # Separate v1.1 API client for media uploads only
            auth = tweepy.OAuth1UserHandler(
                consumer_key=os.environ.get('TWITTER_API_KEY'),
                consumer_secret=os.environ.get('TWITTER_API_SECRET'),
                access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.twitter_api = tweepy.API(auth)
            
            # Verify credentials with 600s delay between retries
            self._verify_credentials()
            
            # Initialize other clients
            self.openai_client = OpenAIClient()
            self.replicate_client = ReplicateClient()
            self.queue = init_queue()
            
            logger.info("TwitterBot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TwitterBot: {str(e)}")
            raise TwitterAPIError(f"Failed to initialize TwitterBot: {str(e)}")

    def _verify_credentials(self):
        """Verify Twitter API credentials and permissions with rate limit handling"""
        base_delay = 600  # 10 minutes base delay
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Check rate limits first
                if not rate_limit_tracker.check_rate_limit('/2/users/me'):
                    wait_time = rate_limit_tracker.get_wait_time('/2/users/me')
                    logger.info(f"Rate limit active, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                
                # Verify v2 access
                me = self.twitter_client.get_me()
                if not me or not hasattr(me, 'data'):
                    raise TwitterAPIError("Failed to verify Twitter API v2 access")
                
                # Update rate limits from response headers
                if hasattr(me, 'response') and hasattr(me.response, 'headers'):
                    rate_limit_tracker.update_limits('/2/users/me', me.response.headers)
                
                # Verify v1.1 access for media operations
                if not self.twitter_api.verify_credentials():
                    raise TwitterAPIError("Failed to verify Twitter API v1.1 access")
                
                logger.info(f"Successfully authenticated as @{me.data.username}")
                return True
                
            except tweepy.errors.TooManyRequests as e:
                wait_time = int(e.response.headers.get('x-rate-limit-reset', base_delay))
                if attempt < max_retries - 1:
                    logger.warning(f"Rate limit hit during verification, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise TwitterAPIError("Rate limit exceeded during verification")
                    
            except Exception as e:
                retry_delay = base_delay * (2 ** attempt)
                logger.error(f"Error verifying credentials (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise TwitterAPIError(f"Failed to verify credentials: {str(e)}")

    def create_post(self):
        """Generate and post new content with comprehensive retry mechanism"""
        max_retries = 3
        base_delay = 900  # 15 minutes base delay
        buffer_time = 300  # Additional 5 minute buffer between retries
        
        for attempt in range(max_retries):
            try:
                # Check rate limits before posting
                if not rate_limit_tracker.check_rate_limit('/2/tweets'):
                    wait_time = rate_limit_tracker.get_wait_time('/2/tweets')
                    logger.info(f"Rate limit active, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                
                prompt = self._generate_post_prompt()
                content = self.openai_client.generate_text(prompt)
                
                # Try creating tweet using v2 endpoint
                response = self.twitter_client.create_tweet(text=content)
                
                # Update rate limits from response headers
                if hasattr(response, 'response') and hasattr(response.response, 'headers'):
                    rate_limit_tracker.update_limits('/2/tweets', response.response.headers)
                
                if not response or 'data' not in response:
                    raise TwitterAPIError("Invalid response from Twitter API")
                
                tweet_id = response['data']['id']
                me = self.twitter_client.get_me()
                username = me['data']['username']
                
                interaction = Interaction(
                    interaction_type="post",
                    tweet_id=tweet_id,
                    user_handle=username,
                    content=content
                )
                db.session.add(interaction)
                db.session.commit()
                logger.info(f"Successfully created tweet: {tweet_id}")
                return
                
            except tweepy.errors.TooManyRequests as e:
                wait_time = int(e.response.headers.get('x-rate-limit-reset', base_delay))
                if attempt < max_retries - 1:
                    logger.warning(f"Rate limit hit, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise TwitterAPIError("Rate limit exceeded after maximum retries")
                    
            except tweepy.errors.Forbidden as e:
                logger.error(f"Permission error creating tweet: {str(e)}")
                if "453" in str(e):  # Access to endpoint restricted
                    raise TwitterAPIError(
                        "Access to this endpoint is restricted. "
                        "Currently have access to a subset of Twitter API V2 endpoints "
                        "and limited v1.1 endpoints only."
                    )
                raise TwitterAPIError(f"Insufficient permissions to create tweet: {str(e)}")
                
            except tweepy.errors.TweepyException as e:
                retry_delay = base_delay * (2 ** attempt) + buffer_time  # Exponential backoff starting at 15 minutes + buffer
                logger.error(f"Twitter API error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise TwitterAPIError(f"Failed to create tweet after {max_retries} attempts: {str(e)}")
                    
            except Exception as e:
                logger.error(f"Unexpected error creating tweet: {str(e)}")
                raise

    def _generate_post_prompt(self):
        """Generate prompt for creating new posts"""
        return """Generate an engaging tweet about technology, AI, art, or creativity. 
        The tweet should be informative, witty, and encourage interaction. 
        Keep it under 280 characters and make it conversational. 
        Include relevant hashtags where appropriate."""

    def handle_reply(self, tweet_id, user_handle, content):
        """Process and respond to replies with error handling"""
        try:
            context = self._get_context()
            should_respond = self._should_respond(content, context)
            
            if should_respond:
                response_type = self._determine_response_type(content)
                
                if response_type == "image":
                    prompt = f"CMONKE {content}"
                    image_url = self.replicate_client.generate_image(prompt)
                    # Download the image and upload using v1.1 API
                    import requests
                    image_data = requests.get(image_url).content
                    media = self.twitter_api.media_upload(filename="response.png", file=image_data)
                    status = self.twitter_api.update_status(
                        status="Here's what I visualized:",
                        in_reply_to_status_id=tweet_id,
                        media_ids=[media.media_id]
                    )
                    response_id = status.id
                    response_text = status.text
                else:
                    response_text = self.openai_client.generate_text(
                        self._generate_reply_prompt(content, context)
                    )
                    status = self.twitter_api.update_status(
                        status=response_text,
                        in_reply_to_status_id=tweet_id
                    )
                    response_id = status.id
                
                self._store_interaction("reply", tweet_id, user_handle, content, 
                                     response_type, response_text)
                logger.info(f"Successfully replied to tweet {tweet_id}")
        except Exception as e:
            logger.error(f"Error handling reply to tweet {tweet_id}: {str(e)}")
            raise

    def handle_mention(self, tweet_id, user_handle, content):
        """Process and respond to mentions"""
        try:
            self.queue.enqueue(self._process_mention, tweet_id, user_handle, content)
            logger.info(f"Queued mention processing for tweet {tweet_id}")
        except Exception as e:
            logger.error(f"Error queueing mention processing: {str(e)}")
            raise

    def _process_mention(self, tweet_id, user_handle, content):
        """Process mention with error handling"""
        try:
            context = self._get_context()
            response_type = self._determine_response_type(content)
            
            if response_type == "image":
                prompt = f"CMONKE {content}"
                image_url = self.replicate_client.generate_image(prompt)
                # Download the image and upload using v1.1 API
                import requests
                image_data = requests.get(image_url).content
                media = self.twitter_api.media_upload(filename="response.png", file=image_data)
                status = self.twitter_api.update_status(
                    status="Here's what I created:",
                    in_reply_to_status_id=tweet_id,
                    media_ids=[media.media_id]
                )
                response_text = status.text
            else:
                response_text = self.openai_client.generate_text(
                    self._generate_mention_prompt(content, context)
                )
                status = self.twitter_api.update_status(
                    status=response_text,
                    in_reply_to_status_id=tweet_id
                )
            
            self._store_interaction("mention", tweet_id, user_handle, content,
                                 response_type, response_text)
            logger.info(f"Successfully processed mention for tweet {tweet_id}")
        except Exception as e:
            logger.error(f"Error processing mention for tweet {tweet_id}: {str(e)}")
            raise

    def _generate_reply_prompt(self, content, context):
        """Generate prompt for replies based on context"""
        return f"""Given this tweet: "{content}"
        And considering the context of our previous interactions,
        generate a friendly and engaging reply that maintains continuity
        of the conversation. Keep it under 280 characters."""

    def _generate_mention_prompt(self, content, context):
        """Generate prompt for mention responses"""
        return f"""Someone mentioned me in this tweet: "{content}"
        Generate an appropriate response that's helpful and engaging.
        Consider the context of any previous interactions.
        Keep it under 280 characters."""

    def _should_respond(self, content, context):
        """Determine if we should respond to this interaction"""
        # Implement logic to avoid spam and repetitive content
        return True

    def _get_context(self):
        """Retrieve last 100 interactions for context"""
        try:
            return Interaction.query.order_by(
                Interaction.created_at.desc()
            ).limit(100).all()
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []

    def _determine_response_type(self, content):
        """Decide whether to respond with text or image"""
        try:
            prompt = f"Analyze this content and decide if it requires an image response or text response. Content: {content}"
            response = self.openai_client.analyze_content(prompt)
            return response['type']  # 'text' or 'image'
        except Exception as e:
            logger.error(f"Error determining response type: {str(e)}")
            return 'text'  # Default to text response on error

    def _store_interaction(self, type, tweet_id, user_handle, content, 
                         response_type, response_content):
        """Store interaction in database"""
        try:
            interaction = Interaction(
                interaction_type=type,
                tweet_id=tweet_id,
                user_handle=user_handle,
                content=content,
                response_type=response_type,
                response_content=response_content
            )
            db.session.add(interaction)
            
            metrics = BotMetrics.query.order_by(BotMetrics.id.desc()).first()
            if not metrics:
                metrics = BotMetrics()
                db.session.add(metrics)
            
            if type == "post":
                metrics.post_count += 1
            elif type == "reply":
                metrics.reply_count += 1
            else:
                metrics.mention_count += 1
                
            if response_type == "image":
                metrics.image_response_count += 1
            else:
                metrics.text_response_count += 1
                
            metrics.updated_at = datetime.utcnow()
            db.session.commit()
            logger.info(f"Successfully stored interaction of type {type}")
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")
            db.session.rollback()
            raise

    def get_stats(self):
        """Get bot statistics for dashboard"""
        try:
            metrics = BotMetrics.query.order_by(BotMetrics.id.desc()).first()
            if not metrics:
                return {
                    "post_count": 0,
                    "reply_count": 0,
                    "mention_count": 0,
                    "image_response_count": 0,
                    "text_response_count": 0
                }
            return {
                "post_count": metrics.post_count,
                "reply_count": metrics.reply_count,
                "mention_count": metrics.mention_count,
                "image_response_count": metrics.image_response_count,
                "text_response_count": metrics.text_response_count
            }
        except Exception as e:
            logger.error(f"Error retrieving stats: {str(e)}")
            return {
                "post_count": 0,
                "reply_count": 0,
                "mention_count": 0,
                "image_response_count": 0,
                "text_response_count": 0
            }