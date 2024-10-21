# app/__init__.py

from flask import Flask
from .auth.oauth import init_oauth
from .auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with a strong secret key



    init_oauth(app)

    # Register blueprints
    app.register_blueprint(auth_bp)

    return app
