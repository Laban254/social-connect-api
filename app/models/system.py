from datetime import datetime
from app import db

class Cache(db.Model):
    __tablename__ = 'cache'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.JSON)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Cache {self.key}>'

class BackgroundTask(db.Model):
    __tablename__ = 'background_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    task_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    priority = db.Column(db.Integer, default=0)
    data = db.Column(db.JSON)
    result = db.Column(db.JSON)
    error = db.Column(db.Text)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BackgroundTask {self.task_type}>'

class RateLimit(db.Model):
    __tablename__ = 'rate_limits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, default=0)
    window_start = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='rate_limits')
    
    def __repr__(self):
        return f'<RateLimit {self.user_id} on {self.endpoint}>'

class SystemConfig(db.Model):
    __tablename__ = 'system_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.JSON)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SystemConfig {self.key}>' 