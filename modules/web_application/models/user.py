from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    social_login_provider = db.Column(db.String(50))
    profile_picture = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    scraped_data = db.relationship('ScrapedData', backref='user', lazy=True)
    prompt_logs = db.relationship('PromptLog', backref='user', lazy=True)

