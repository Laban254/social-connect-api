import pytest
from app import create_app
from app.models import db
import os

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    
    # Create the database and load test data
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def auth_headers():
    """Generate authentication headers for testing."""
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    } 