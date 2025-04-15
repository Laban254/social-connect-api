from datetime import datetime
from app import db

class ContentFeed(db.Model):
    __tablename__ = 'content_feeds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False)  # post, story, poll, event
    content_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='content_feeds')
    
    def __repr__(self):
        return f'<ContentFeed {self.content_type} {self.content_id}>'

class SearchIndex(db.Model):
    __tablename__ = 'search_index'
    
    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(20), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    tags = db.Column(db.JSON)  # Store as JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SearchIndex {self.content_type} {self.content_id}>'

class ContentModeration(db.Model):
    __tablename__ = 'content_moderation'
    
    id = db.Column(db.Integer, primary_key=True)
    content_type = db.Column(db.String(20), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # report, hide, delete
    reason = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='content_moderations')
    
    def __repr__(self):
        return f'<ContentModeration {self.action} on {self.content_type} {self.content_id}>'

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='audit_logs')
    
    def __repr__(self):
        return f'<AuditLog {self.action} by {self.user_id}>' 