from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middleware import limiter
from app.metrics import ACTIVE_USERS
import time

api_bp = Blueprint('api', __name__)

@api_bp.route('/protected', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")
def protected():
    """Example protected endpoint."""
    current_user = get_jwt_identity()
    return jsonify({
        'message': f'Hello {current_user}!',
        'status': 'success'
    })

@api_bp.route('/users', methods=['GET'])
@jwt_required()
@limiter.limit("20 per minute")
def get_users():
    """Get all users."""
    # Simulate database query
    time.sleep(0.1)
    return jsonify({
        'users': [
            {'id': 1, 'name': 'John Doe'},
            {'id': 2, 'name': 'Jane Smith'}
        ]
    })

@api_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@limiter.limit("30 per minute")
def get_user(user_id):
    """Get a specific user."""
    # Simulate database query
    time.sleep(0.05)
    return jsonify({
        'id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com'
    })

@api_bp.route('/error', methods=['GET'])
def trigger_error():
    """Endpoint to trigger an error for testing."""
    raise Exception("This is a test error") 