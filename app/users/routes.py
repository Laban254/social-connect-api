from flask import Blueprint, request, jsonify
from app.users.services import update_user_profile, follow_user_service, unfollow_user_service, is_following
from app.users.models import User
from app.utils.auth import get_current_user_id

users_bp = Blueprint('users', __name__)

@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    current_user_id = get_current_user_id()

    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized to update this profile'}), 403

    data = request.json
    name = data.get('name')
    profile_pic = data.get('profile_pic')
    is_private = data.get('is_private')

    user = update_user_profile(user_id, name=name, profile_pic=profile_pic, is_private=is_private)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'profile_pic': user.profile_pic,
            'is_private': user.is_private
        }
    }), 200

@users_bp.route('/users/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    current_user_id = get_current_user_id()

    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    if follow_user_service(current_user_id, user_id):
        return jsonify({'message': f'You are now following user {user_id}'}), 201
    else:
        return jsonify({'message': 'Already following'}), 400

@users_bp.route('/users/<int:user_id>/unfollow', methods=['POST'])
def unfollow_user(user_id):
    current_user_id = get_current_user_id()

    if not current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    if unfollow_user_service(current_user_id, user_id):
        return jsonify({'message': f'You have unfollowed user {user_id}'}), 200
    else:
        return jsonify({'message': 'You are not following this user'}), 400

@users_bp.route('/users/<int:followed_id>/is_following', methods=['GET'])
def check_is_following(followed_id):
    follower_id = get_current_user_id()

    if not follower_id or not User.query.get(follower_id) or not User.query.get(followed_id):
        return jsonify({'error': 'Invalid user ID'}), 400

    is_following_status = is_following(follower_id, followed_id)
    return jsonify({'is_following': is_following_status}), 200
