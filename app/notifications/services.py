from app.extensions import db
from app.notifications.models import Notification

def get_notifications(user_id):
    # Get unread notifications for the user
    return Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()

def mark_as_read(user_id, notification_id):
    # Find notification by ID and user ID
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if notification:
        notification.is_read = True
        db.session.commit()
        return True
    return False

def create_notification(user_id, message):
    # Create a new notification
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()

    # WebSocket trigger for real-time delivery
    from app.notifications.websocket import send_notification
    send_notification(user_id, message)
