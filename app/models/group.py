from datetime import datetime
from app import db

class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_private = db.Column(db.Boolean, default=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    members = db.relationship('GroupMember', back_populates='group', cascade='all, delete-orphan')
    events = db.relationship('GroupEvent', back_populates='group', cascade='all, delete-orphan')
    discussions = db.relationship('GroupDiscussion', back_populates='group', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Group {self.name}>'

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # member, moderator, admin
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='members')
    user = db.relationship('User', backref='group_memberships')
    
    def __repr__(self):
        return f'<GroupMember {self.user_id} in {self.group_id}>'

class GroupEvent(db.Model):
    __tablename__ = 'group_events'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='events')
    attendees = db.relationship('EventAttendee', back_populates='event', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<GroupEvent {self.title}>'

class EventAttendee(db.Model):
    __tablename__ = 'event_attendees'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('group_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, going, not_going
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    event = db.relationship('GroupEvent', back_populates='attendees')
    user = db.relationship('User', backref='event_attendances')
    
    def __repr__(self):
        return f'<EventAttendee {self.user_id} for {self.event_id}>'

class GroupDiscussion(db.Model):
    __tablename__ = 'group_discussions'
    
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    group = db.relationship('Group', back_populates='discussions')
    comments = db.relationship('DiscussionComment', back_populates='discussion', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<GroupDiscussion {self.title}>'

class DiscussionComment(db.Model):
    __tablename__ = 'discussion_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    discussion_id = db.Column(db.Integer, db.ForeignKey('group_discussions.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    discussion = db.relationship('GroupDiscussion', back_populates='comments')
    user = db.relationship('User', backref='discussion_comments')
    
    def __repr__(self):
        return f'<DiscussionComment {self.id}>' 