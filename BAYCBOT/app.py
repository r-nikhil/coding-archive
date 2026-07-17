import os
from flask import Flask, render_template
from database import db
from queue_manager import init_queue
from bot import TwitterBot

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    db.init_app(app)
    return app

app = create_app()

# Initialize bot instance
bot = TwitterBot()
queue = init_queue()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    stats = bot.get_stats()
    return stats

with app.app_context():
    import models
    db.create_all()
