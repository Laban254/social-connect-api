from flask import request, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import time
import logging

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def setup_middleware(app):
    @app.before_request
    def before_request():
        g.start = time.time()
        g.request_id = request.headers.get('X-Request-ID', 'no-request-id')
        
        # Log request details
        app.logger.info(f"Request started: {request.method} {request.path} - ID: {g.request_id}")
        
        # Add security headers
        @app.after_request
        def add_security_headers(response):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            return response
    
    @app.after_request
    def after_request(response):
        # Calculate request duration
        duration = time.time() - g.start
        
        # Log response details
        app.logger.info(
            f"Request completed: {request.method} {request.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.2f}s - "
            f"ID: {g.request_id}"
        )
        
        return response 