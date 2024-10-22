from app.extensions import db
from app.interactions.models import Like, Comment
# from app.notifications.services import trigger_notification  # Assuming a notification service exists

def like_post(user_id, post_id):
    """Add a like to a post by the given user."""
    try:
        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        if existing_like:
            return False  # User has already liked the post
        
        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        
        # Optionally trigger a notification for the post's author
        # trigger_notification(post_id, f'User {user_id} liked your post.')
        
        return True
    except Exception as e:
        db.session.rollback()  
        raise e 

def comment_on_post(user_id, post_id, content):
    """Add a comment to a post by the given user."""
    try:
        new_comment = Comment(user_id=user_id, post_id=post_id, content=content)
        db.session.add(new_comment)
        db.session.commit()
        
        # Optionally trigger a notification for the post's author
        # trigger_notification(post_id, f'User {user_id} commented on your post: "{content}"')

        return new_comment
    except Exception as e:
        db.session.rollback()  
        raise e
