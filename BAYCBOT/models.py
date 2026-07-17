from datetime import datetime
from database import db

class Interaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interaction_type = db.Column(db.String(20), nullable=False)  # post, reply, mention
    tweet_id = db.Column(db.String(50), nullable=False)
    user_handle = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    response_type = db.Column(db.String(20))  # text, image
    response_content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Context(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interaction_id = db.Column(db.Integer, db.ForeignKey('interaction.id'))
    context_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BotMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_count = db.Column(db.Integer, default=0)
    reply_count = db.Column(db.Integer, default=0)
    mention_count = db.Column(db.Integer, default=0)
    image_response_count = db.Column(db.Integer, default=0)
    text_response_count = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
