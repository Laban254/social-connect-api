import pytest
from app.models import User

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}

def test_rate_limiting(client):
    """Test rate limiting functionality."""
    # Make multiple requests to trigger rate limiting
    for _ in range(60):
        response = client.get('/health')
    
    # Next request should be rate limited
    response = client.get('/health')
    assert response.status_code == 429

def test_authentication(client, auth_headers):
    """Test authentication endpoints."""
    # Test login
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json

    # Test protected endpoint
    response = client.get('/api/protected', headers=auth_headers)
    assert response.status_code == 200

def test_error_handling(client):
    """Test error handling."""
    # Test 404
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    # Test 500
    response = client.get('/error')
    assert response.status_code == 500 