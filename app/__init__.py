# app/__init__.py

from flask import Flask
from .auth.oauth import init_oauth
from .auth.routes import auth_bp
from app.config import Config

config = Config()

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY  

    init_oauth(app)

    app.register_blueprint(auth_bp)

    return app
