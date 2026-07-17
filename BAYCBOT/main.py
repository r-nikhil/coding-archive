from app import app, bot, queue
import time
import threading
import logging
import subprocess
import os
import signal
from bot import TwitterAPIError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_bot():
    consecutive_errors = 0
    max_consecutive_errors = 5
    base_delay = 300  # 5 minutes
    
    while True:
        try:
            # Create new post every 4 hours
            bot.create_post()
            consecutive_errors = 0  # Reset error counter on success
            logger.info("Successfully created new post")
            time.sleep(14400)  # 4 hours
        except TwitterAPIError as e:
            logger.error(f"Twitter API Error: {str(e)}")
            # For API permission errors, we should stop the bot
            logger.critical("Stopping bot due to API permission error")
            break
        except Exception as e:
            consecutive_errors += 1
            delay = min(base_delay * (2 ** consecutive_errors), 3600)  # Max 1 hour delay
            logger.error(f"Error in bot thread (attempt {consecutive_errors}): {str(e)}")
            
            if consecutive_errors >= max_consecutive_errors:
                logger.critical(f"Bot stopped after {consecutive_errors} consecutive errors")
                break
                
            logger.info(f"Waiting {delay} seconds before retry")
            time.sleep(delay)

# Redis server is handled by system dependencies

if __name__ == "__main__":
    try:
        # Configure detailed logging first
        logging.getLogger('werkzeug').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        logger.setLevel(logging.DEBUG)
        logger.info("Starting application in debug mode...")

        # Step 1: Verify environment variables
        logger.info("Verifying environment variables...")
        required_vars = [
            'TWITTER_API_KEY', 'TWITTER_API_SECRET',
            'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET',
            'TWITTER_BEARER_TOKEN', 'OPENAI_API_KEY',
            'REPLICATE_API_TOKEN', 'DATABASE_URL'
        ]
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.info("✓ Environment variables verified successfully")

        # Step 2: Verify database connection with timeout
        logger.info("Verifying database connection...")
        from sqlalchemy import create_engine
        from sqlalchemy.exc import SQLAlchemyError
        import threading
        import queue as Queue

        def test_db_connection():
            try:
                with app.app_context():
                    db.engine.connect()
                    import models
                    db.create_all()
                return True
            except Exception as e:
                return e

        # Use a queue to handle the timeout
        q = Queue.Queue()
        db_thread = threading.Thread(target=lambda: q.put(test_db_connection()))
        db_thread.daemon = True
        db_thread.start()
        db_thread.join(timeout=10)  # 10 second timeout

        if db_thread.is_alive():
            raise TimeoutError("Database connection timed out after 10 seconds")

        result = q.get()
        if isinstance(result, Exception):
            raise result
        logger.info("✓ Database connection and tables verified")

        # Step 3: Start Flask app in debug mode
        logger.info("Starting Flask application in debug mode...")
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'connect_args': {'connect_timeout': 10}
        }
        app.run(host="0.0.0.0", port=5000, debug=True)

    except ValueError as ve:
        logger.critical(f"Configuration error: {str(ve)}")
        raise
    except TimeoutError as te:
        logger.critical(f"Timeout error: {str(te)}")
        raise
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}", exc_info=True)
        raise
