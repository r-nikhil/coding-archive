import os
import time
import socket
import logging
from rq import Queue
import redis
from redis.exceptions import ConnectionError as RedisConnectionError, TimeoutError as RedisTimeoutError
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

logger = logging.getLogger(__name__)

def init_queue():
    """Initialize Redis queue with proper error handling"""
    try:
        # Get Redis configuration from environment
        redis_host = os.environ.get('REDIS_HOST')
        redis_port = os.environ.get('REDIS_PORT')
        redis_password = os.environ.get('REDIS_PASSWORD')

        if not all([redis_host, redis_port, redis_password]):
            missing_vars = []
            if not redis_host: missing_vars.append('REDIS_HOST')
            if not redis_port: missing_vars.append('REDIS_PORT')
            if not redis_password: missing_vars.append('REDIS_PASSWORD')
            error_msg = f"Missing Redis configuration: {', '.join(missing_vars)}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Log connection attempt
        logger.info(f"Attempting to connect to Redis at {redis_host}:{redis_port}")
        logger.debug(f"Using Redis port from environment: {redis_port}")

        # Construct Redis URL with proper formatting
        redis_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"

        # Configure retry strategy with exponential backoff
        retry = Retry(ExponentialBackoff(cap=10, base=1), 3)

        # Initialize Redis connection with updated configuration
        redis_conn = redis.from_url(
            redis_url,
            decode_responses=False,  # Required for RQ compatibility
            socket_timeout=30,       # Updated as requested
            socket_connect_timeout=20,  # Updated as requested
            socket_keepalive=True,   # Added as requested
            retry_on_timeout=True,
            retry=retry,
            health_check_interval=30
        )
        
        # Test connection with retry logic
        for attempt in range(3):
            try:
                logger.info(f"Testing Redis connection (attempt {attempt + 1}/3)")
                redis_conn.ping()
                logger.info("Successfully connected to Redis")
                break
            except (RedisConnectionError, RedisTimeoutError) as e:
                if attempt == 2:  # Last attempt
                    logger.error(f"Failed to connect to Redis after 3 attempts: {str(e)}")
                    raise
                delay = min(2 ** attempt, 10)  # Exponential backoff capped at 10 seconds
                logger.warning(f"Redis connection attempt {attempt + 1} failed, retrying in {delay} seconds...")
                time.sleep(delay)
        
        # Initialize RQ queue with updated settings
        queue = Queue(
            name='twitter_bot_queue',
            connection=redis_conn,
            default_timeout=360,
            job_timeout=180,
            result_ttl=86400,  # Keep results for 1 day
            failure_ttl=86400  # Keep failed jobs for 1 day
        )
        
        return queue
                
    except RedisConnectionError as e:
        logger.error(f"Redis connection error: {str(e)}")
        raise
    except RedisTimeoutError as e:
        logger.error(f"Redis timeout error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error initializing queue: {str(e)}")
        raise
