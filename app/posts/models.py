# app/posts/models.py

from app import db 
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255), nullable=True) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    hashtags = db.relationship('Hashtag', secondary='post_hashtag', back_populates='posts')
    likes = db.relationship('Like', back_populates='post', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Post {self.id}>'

class Hashtag(db.Model):
    __tablename__ = 'hashtags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Post', secondary='post_hashtag', back_populates='hashtags')

class PostHashtag(db.Model):
    __tablename__ = 'post_hashtag'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    hashtag_id = db.Column(db.Integer, db.ForeignKey('hashtags.id'), primary_key=True)
