from flask import Flask
from .auth.oauth import init_oauth
from .auth.routes import auth_bp
from .users.routes import  users_bp
from app.config import Config
from app.extensions import db, migrate
from .posts.routes import posts_bp

config = Config()

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY
    
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    init_oauth(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(posts_bp)



    return app