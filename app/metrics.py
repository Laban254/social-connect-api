from prometheus_client import Counter, Histogram, Gauge
import time
from flask import request

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

def setup_metrics(app):
    @app.before_request
    def before_request():
        request.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        # Record request count
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint,
            status=response.status_code
        ).inc()
        
        # Record request latency
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.endpoint
        ).observe(time.time() - request.start_time)
        
        return response 