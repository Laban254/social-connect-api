import logging
import os
from logging.handlers import RotatingFileHandler
from flask import current_app

def setup_logger(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/social_connect.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to the app's logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    # Log startup message
    app.logger.info('Social Connect API startup') 