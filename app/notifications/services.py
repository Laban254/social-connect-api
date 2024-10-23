from app.extensions import db
from app.notifications.models import Notification
from app.posts.models import Post

def get_notifications(user_id):
    print(f"Getting notifications for user_id: {user_id}")
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
    print(f"Found {len(notifications)} notifications.")
    return notifications

def mark_as_read(user_id, notification_id):
    print(f"Marking notification {notification_id} as read for user_id: {user_id}")
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if notification:
        notification.is_read = True
        db.session.commit()
        print(f"Notification {notification_id} marked as read.")
        return True
    print(f"Notification {notification_id} not found for user_id: {user_id}.")
    return False

def create_notification(user_id, message):
    print(f"Creating notification for user_id: {user_id} with message: {message}")
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()
    print(f"Notification created with ID: {notification.id}")

    from app.notifications.websocket import send_notification
    send_notification(user_id, message)

def get_post_author_id(post_id):
    print(f"Getting author ID for post_id: {post_id}")
    post = Post.query.filter_by(id=post_id).first()
    if post:
        print(f"Found post with ID: {post.id}, author ID: {post.id}")
        return post.id  
    print(f"Post with ID: {post_id} not found.")
    return None

def trigger_notification(post_id, message):
    print(f"Triggering notification for post_id: {post_id} with message: {message}")
    post_author_id = get_post_author_id(post_id)
    if post_author_id:
        create_notification(post_author_id, message)
    else:
        print(f"No author found for post_id: {post_id}")
