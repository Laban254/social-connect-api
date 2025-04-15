from datetime import datetime
from app import db

class UserAnalytics(db.Model):
    __tablename__ = 'user_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    active_time = db.Column(db.Integer, default=0)  # in minutes
    post_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    story_views = db.Column(db.Integer, default=0)
    poll_participation = db.Column(db.Integer, default=0)
    event_attendance = db.Column(db.Integer, default=0)
    
    # Relationships
    user = db.relationship('User', backref='analytics')
    
    def __repr__(self):
        return f'<UserAnalytics {self.user_id} for {self.date}>'

class ContentAnalytics(db.Model):
    __tablename__ = 'content_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, nullable=False)  # Generic foreign key
    content_type = db.Column(db.String(20), nullable=False)  # post, story, poll, event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    reach = db.Column(db.Integer, default=0)
    
    # Relationships
    user = db.relationship('User', backref='content_analytics')
    
    def __repr__(self):
        return f'<ContentAnalytics {self.content_type} {self.content_id}>'

class AudienceInsight(db.Model):
    __tablename__ = 'audience_insights'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    age_group = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    location = db.Column(db.String(100))
    interests = db.Column(db.JSON)  # Store as JSON array
    active_hours = db.Column(db.JSON)  # Store as JSON object with hour:count pairs
    device_type = db.Column(db.String(20))
    
    # Relationships
    user = db.relationship('User', backref='audience_insights')
    
    def __repr__(self):
        return f'<AudienceInsight {self.user_id} for {self.date}>'

class APIAnalytics(db.Model):
    __tablename__ = 'api_analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response_time = db.Column(db.Float)  # in milliseconds
    status_code = db.Column(db.Integer)
    request_size = db.Column(db.Integer)  # in bytes
    response_size = db.Column(db.Integer)  # in bytes
    
    # Relationships
    user = db.relationship('User', backref='api_analytics')
    
    def __repr__(self):
        return f'<APIAnalytics {self.endpoint} at {self.timestamp}>'

class CustomReport(db.Model):
    __tablename__ = 'custom_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50), nullable=False)  # user, content, audience, api
    parameters = db.Column(db.JSON)  # Store report configuration
    schedule = db.Column(db.String(50))  # daily, weekly, monthly, custom
    last_generated = db.Column(db.DateTime)
    next_generation = db.Column(db.DateTime)
    export_format = db.Column(db.String(20))  # csv, json, pdf
    
    # Relationships
    user = db.relationship('User', backref='custom_reports')
    
    def __repr__(self):
        return f'<CustomReport {self.name}>' 