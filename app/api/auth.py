from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.api import api
from app.schemas.user import user_schema
from app.utils.decorators import validate_json
from app.utils.rate_limit import rate_limit

@api.route('/auth/register', methods=['POST'])
@validate_json({
    'username': {'type': 'string', 'required': True, 'minlength': 3},
    'email': {'type': 'string', 'required': True, 'format': 'email'},
    'password': {'type': 'string', 'required': True, 'minlength': 8}
})
@rate_limit(limit=5, period=300)  # 5 requests per 5 minutes
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
        
    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user_schema.dump(user)
    }), 201

@api.route('/auth/login', methods=['POST'])
@validate_json({
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
})
@rate_limit(limit=10, period=300)  # 10 requests per 5 minutes
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
        
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user_schema.dump(user)
    })

@api.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    
    return jsonify({'access_token': access_token})

@api.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify({'user': user_schema.dump(user)}) 