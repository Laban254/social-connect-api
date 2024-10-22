import requests
from flask import request, jsonify
from app.users.models import User

def validate_google_token(token):
    try:
        response = requests.get(f'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token={token}')
        if response.status_code != 200:
            return None

        return response.json()
    except Exception:
        return None

def get_current_user_id():
    token = request.headers.get('Authorization')
    if token:
        try:
            token = token.split(" ")[1]
            token_info = validate_google_token(token)

            if token_info and 'email' in token_info:
                email = token_info['email']
                user = User.query.filter_by(email=email).first()  
                if user:
                    return user.id  
        except Exception:
            return None
    return None
