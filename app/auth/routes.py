from flask import Blueprint, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from .oauth import oauth
from app.users.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return '<a href="/login">Login with Google</a>'

@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.auth_callback', _external=True) 
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/auth/callback')
def auth_callback():  
    try:
        token = oauth.google.authorize_access_token()  
        resp = oauth.google.get('userinfo')
        user_info = resp.json()

        user = User.query.filter_by(email=user_info['email']).first()
        
        if not user:
            new_user = User(
                email=user_info['email'],
                name=user_info['name'],
                profile_pic=user_info.get('picture')
            )
            db.session.add(new_user)
            db.session.commit()  

        session['user'] = user_info  
        session['token'] = token  

        return jsonify({
            "access_token": token.get('access_token'),  
            "user_info": user_info
        })

    except Exception as e:
        return f"Error during authentication: {e}", 400

@auth_bp.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return jsonify({"user_info": user})
    return jsonify({"error": "User not logged in"}), 401

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully"})
