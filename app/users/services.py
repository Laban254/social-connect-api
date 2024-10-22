# app/users/services.py

from app.users.models import User, Follows
from app.extensions import db

def update_user_profile(user_id, name=None, profile_pic=None, is_private=None):
    user = User.query.get(user_id)
    if not user:
        return None
    
    if name:
        user.name = name
    if profile_pic:
        user.profile_pic = profile_pic
    if is_private is not None:
        user.is_private = is_private
    
    db.session.commit()
    return user

def is_following(follower_id, followed_id):
    return Follows.query.filter_by(follower_id=follower_id, followed_id=followed_id).count() > 0

def follow_user_service(follower_id, followed_id):
    if is_following(follower_id, followed_id):
        return False
    
    new_follow = Follows(follower_id=follower_id, followed_id=followed_id)
    db.session.add(new_follow)
    db.session.commit()
    return True

def unfollow_user_service(follower_id, followed_id):
    follow_relationship = Follows.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
    if not follow_relationship:
        return False
    
    db.session.delete(follow_relationship)
    db.session.commit()
    return True
