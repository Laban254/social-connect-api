from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import os
from flask_socketio import SocketIO
from .auth.oauth import init_oauth
from app.config import Config
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from werkzeug.middleware.proxy_fix import ProxyFix

socketio = SocketIO()  # Initialize SocketIO

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
metrics = PrometheusMetrics.for_app_factory()

def create_app(config_object=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_object is None:
        app.config.from_object('app.config.DevelopmentConfig')
    else:
        app.config.from_object(config_object)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    CORS(app)
    metrics.init_app(app)
    
    # Setup logging
    from app.logger import setup_logger
    setup_logger(app)
    
    # Setup middleware
    from app.middleware import setup_middleware
    setup_middleware(app)
    
    # Setup metrics
    from app.metrics import setup_metrics
    setup_metrics(app)
    
    # Add prometheus metrics endpoint
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    
    # Apply middleware
    app.wsgi_app = ProxyFix(app.wsgi_app)
    
    # Register blueprints
    from app.api import api
    app.register_blueprint(api)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Initialize monitoring
    from app.monitoring import init_monitoring
    init_monitoring(app)
    
    # Initialize background tasks
    from app.services.tasks import init_tasks
    init_tasks(app)
    
    # Initialize SocketIO with the app
    socketio.init_app(app)

    return app
