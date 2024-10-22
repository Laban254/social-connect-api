from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(200)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_private = db.Column(db.Boolean, default=False)  

    followers = db.relationship(
        'User', 
        secondary='follows',
        primaryjoin='User.id == Follows.followed_id',
        secondaryjoin='User.id == Follows.follower_id',
        backref='following',
        lazy='dynamic'
    )

    def __init__(self, email, name, profile_pic=None, is_private=False):
        self.email = email
        self.name = name
        self.profile_pic = profile_pic
        self.is_private = is_private

class Follows(db.Model):
    __tablename__ = 'follows'
    
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
