from datetime import datetime
from app import db

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='events')
    attendees = db.relationship('EventAttendee', back_populates='event', cascade='all, delete-orphan')
    reminders = db.relationship('EventReminder', back_populates='event', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'

class EventAttendee(db.Model):
    __tablename__ = 'event_attendees'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # going, maybe, not_going
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    event = db.relationship('Event', back_populates='attendees')
    user = db.relationship('User', backref='event_attendances')
    
    def __repr__(self):
        return f'<EventAttendee {self.user_id} for {self.event_id}>'

class EventReminder(db.Model):
    __tablename__ = 'event_reminders'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    event = db.relationship('Event', back_populates='reminders')
    user = db.relationship('User', backref='event_reminders')
    
    def __repr__(self):
        return f'<EventReminder {self.id}>' 