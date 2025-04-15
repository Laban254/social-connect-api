from datetime import datetime, timedelta
from app import db

class Story(db.Model):
    __tablename__ = 'stories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    media_url = db.Column(db.String(255))
    media_type = db.Column(db.String(20))  # image, video, text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))
    
    # Relationships
    user = db.relationship('User', backref='stories')
    reactions = db.relationship('StoryReaction', back_populates='story', cascade='all, delete-orphan')
    replies = db.relationship('StoryReply', back_populates='story', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Story {self.id}>'

class StoryReaction(db.Model):
    __tablename__ = 'story_reactions'
    
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reaction_type = db.Column(db.String(20), nullable=False)  # like, love, laugh, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    story = db.relationship('Story', back_populates='reactions')
    user = db.relationship('User', backref='story_reactions')
    
    def __repr__(self):
        return f'<StoryReaction {self.id}>'

class StoryReply(db.Model):
    __tablename__ = 'story_replies'
    
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    story = db.relationship('Story', back_populates='replies')
    user = db.relationship('User', backref='story_replies')
    
    def __repr__(self):
        return f'<StoryReply {self.id}>'

class Poll(db.Model):
    __tablename__ = 'polls'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='polls')
    options = db.relationship('PollOption', back_populates='poll', cascade='all, delete-orphan')
    votes = db.relationship('PollVote', back_populates='poll', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Poll {self.id}>'

class PollOption(db.Model):
    __tablename__ = 'poll_options'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    
    # Relationships
    poll = db.relationship('Poll', back_populates='options')
    votes = db.relationship('PollVote', back_populates='option', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PollOption {self.id}>'

class PollVote(db.Model):
    __tablename__ = 'poll_votes'
    
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('polls.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('poll_options.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    poll = db.relationship('Poll', back_populates='votes')
    option = db.relationship('PollOption', back_populates='votes')
    user = db.relationship('User', backref='poll_votes')
    
    def __repr__(self):
        return f'<PollVote {self.id}>'

class Survey(db.Model):
    __tablename__ = 'surveys'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='surveys')
    questions = db.relationship('SurveyQuestion', back_populates='survey', cascade='all, delete-orphan')
    responses = db.relationship('SurveyResponse', back_populates='survey', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Survey {self.id}>'

class SurveyQuestion(db.Model):
    __tablename__ = 'survey_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), nullable=False)  # text, multiple_choice, rating
    is_required = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer)
    
    # Relationships
    survey = db.relationship('Survey', back_populates='questions')
    options = db.relationship('SurveyOption', back_populates='question', cascade='all, delete-orphan')
    responses = db.relationship('SurveyResponse', back_populates='question', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SurveyQuestion {self.id}>'

class SurveyOption(db.Model):
    __tablename__ = 'survey_options'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('survey_questions.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer)
    
    # Relationships
    question = db.relationship('SurveyQuestion', back_populates='options')
    responses = db.relationship('SurveyResponse', back_populates='option', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<SurveyOption {self.id}>'

class SurveyResponse(db.Model):
    __tablename__ = 'survey_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('survey_questions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('survey_options.id'))
    text_response = db.Column(db.Text)
    rating_response = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    survey = db.relationship('Survey', back_populates='responses')
    question = db.relationship('SurveyQuestion', back_populates='responses')
    option = db.relationship('SurveyOption', back_populates='responses')
    user = db.relationship('User', backref='survey_responses')
    
    def __repr__(self):
        return f'<SurveyResponse {self.id}>' 