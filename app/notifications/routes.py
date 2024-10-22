from flask import Blueprint, jsonify
from app.notifications.services import get_notifications, mark_as_read
from app.utils.auth import get_current_user_id

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications', methods=['GET'])
def get_user_notifications():
    current_user_id = get_current_user_id()
    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    notifications = get_notifications(current_user_id)
    return jsonify([{
        'id': notification.id,
        'message': notification.message,
        'is_read': notification.is_read,
        'timestamp': notification.timestamp
    } for notification in notifications]), 200

@notifications_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_as_read(notification_id):
    current_user_id = get_current_user_id()
    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    success = mark_as_read(current_user_id, notification_id)
    if not success:
        return jsonify({'error': 'Notification not found or unauthorized'}), 404

    return jsonify({'message': 'Notification marked as read'}), 200
