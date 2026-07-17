
from flask import Flask, request, jsonify, render_template, session
from datetime import timedelta
from twitter_bot import TwitterBot
import logging
import json
import os

# Configure logging with more details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def init_twitter_bot():
    """Initialize TwitterBot with proper error handling"""
    try:
        logger.info("Starting TwitterBot initialization")
        
        if not os.path.exists('config.json'):
            logger.info("Creating new config.json file")
            with open('config.json', 'w') as f:
                json.dump({'twitter_cookies': {}}, f)
        
        with open('config.json', 'r') as f:
            config = json.load(f)
            twitter_cookies = config.get('twitter_cookies', {})
            
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        return twitter_cookies
        
    except Exception as e:
        logger.error(f"Failed to initialize Twitter configuration: {str(e)}")
        return {}

logger.info("Starting Flask application setup")
twitter_cookies = init_twitter_bot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post_meme', methods=['POST'])
def post_meme():
    try:
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({'error': 'No image file uploaded'}), 400
            
        try:
            bot = TwitterBot(cookies=twitter_cookies)
        except Exception as e:
            logger.error(f"Failed to initialize TwitterBot: {str(e)}")
            return jsonify({'error': 'Failed to initialize Twitter bot'}), 500
            
        image = request.files['image']
        if image.filename == '':
            logger.error("Empty filename in request")
            return jsonify({'error': 'No selected file'}), 400
            
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            logger.error(f"Invalid file type: {image.filename}")
            return jsonify({'error': 'Invalid file type. Allowed types: PNG, JPG, JPEG, GIF'}), 400
            
        from werkzeug.utils import secure_filename
        filename = secure_filename(image.filename)
        
        upload_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
        os.makedirs(upload_folder, exist_ok=True)
        
        import uuid
        unique_filename = f"{uuid.uuid4()}_{filename}"
        image_path = os.path.join(upload_folder, unique_filename)
        
        try:
            image.save(image_path)
            logger.info(f"Saved uploaded file to: {image_path}")
            
            if not os.path.exists(image_path):
                raise FileNotFoundError("Failed to save uploaded file")
                
            file_size = os.path.getsize(image_path)
            if file_size == 0:
                raise ValueError("Uploaded file is empty")
                
            tweet_data = {
                'tweet_id': request.form.get('tweet_id'),
                'username': request.form.get('username'),
                'image_path': image_path
            }

            success = bot.post_reply_with_meme(tweet_data)
            
            try:
                os.remove(image_path)
            except Exception as e:
                logger.warning(f"Failed to cleanup uploaded file: {str(e)}")
            
            if success:
                return jsonify({'message': 'Successfully posted meme reply'}), 200
            else:
                return jsonify({'error': 'Failed to post meme reply'}), 500

        except Exception as e:
            logger.error(f"Error processing upload: {str(e)}")
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        logger.error(f"Error in post_meme: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
