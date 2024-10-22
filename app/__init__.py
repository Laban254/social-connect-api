from flask import Flask
from flask_socketio import SocketIO
from .auth.oauth import init_oauth
from .auth.routes import auth_bp
from .users.routes import users_bp
from .posts.routes import posts_bp
from .interactions.routes import interactions_bp
from app.config import Config
from app.extensions import db, migrate

socketio = SocketIO()  # Initialize SocketIO

config = Config()

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    init_oauth(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(interactions_bp)

    # Initialize SocketIO with the app
    socketio.init_app(app)

    return app
