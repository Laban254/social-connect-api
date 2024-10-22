from app.extensions import db 
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(200))  # Optional, for profile picture URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, name, profile_pic=None):
        self.email = email
        self.name = name
        self.profile_pic = profile_pic