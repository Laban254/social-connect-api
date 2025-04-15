from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.api import api
from app.schemas.user import user_schema, users_schema
from app.utils.decorators import validate_json
from app.utils.rate_limit import rate_limit

@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'user': user_schema.dump(user)})

@api.route('/users/me', methods=['PUT'])
@jwt_required()
@validate_json({
    'username': {'type': 'string', 'minlength': 3},
    'email': {'type': 'string', 'format': 'email'},
    'bio': {'type': 'string'},
    'profile_picture': {'type': 'string'}
})
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    data = request.get_json()
    
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        user.username = data['username']
        
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']
        
    if 'bio' in data:
        user.bio = data['bio']
        
    if 'profile_picture' in data:
        user.profile_picture = data['profile_picture']
        
    db.session.commit()
    return jsonify({'user': user_schema.dump(user)})

@api.route('/users/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user_id = get_jwt_identity()
    user_to_follow = User.query.get_or_404(user_id)
    current_user = User.query.get(current_user_id)
    
    if current_user.id == user_id:
        return jsonify({'error': 'Cannot follow yourself'}), 400
        
    if user_to_follow in current_user.following:
        return jsonify({'error': 'Already following this user'}), 400
        
    current_user.follow(user_to_follow)
    db.session.commit()
    
    return jsonify({'message': f'Successfully followed {user_to_follow.username}'})

@api.route('/users/<int:user_id>/unfollow', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user_id = get_jwt_identity()
    user_to_unfollow = User.query.get_or_404(user_id)
    current_user = User.query.get(current_user_id)
    
    if user_to_unfollow not in current_user.following:
        return jsonify({'error': 'Not following this user'}), 400
        
    current_user.unfollow(user_to_unfollow)
    db.session.commit()
    
    return jsonify({'message': f'Successfully unfollowed {user_to_unfollow.username}'})

@api.route('/users/<int:user_id>/followers', methods=['GET'])
@jwt_required()
def get_followers(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'followers': users_schema.dump(user.followers)})

@api.route('/users/<int:user_id>/following', methods=['GET'])
@jwt_required()
def get_following(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'following': users_schema.dump(user.following)})

@api.route('/users/search', methods=['GET'])
@jwt_required()
def search_users():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
        
    users = User.query.filter(
        (User.username.ilike(f'%{query}%')) |
        (User.email.ilike(f'%{query}%'))
    ).all()
    
    return jsonify({'users': users_schema.dump(users)}) 