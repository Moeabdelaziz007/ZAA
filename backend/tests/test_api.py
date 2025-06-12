import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from zero_system import ZeroSystem

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers(client):
    """Get authentication headers by logging in."""
    response = client.post('/api/auth/login', 
                          json={'username': 'admin', 'password': 'admin123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    token = data['access_token']
    return {'Authorization': f'Bearer {token}'}

class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test that health check returns 200."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

class TestAuthentication:
    """Test authentication endpoints."""
    
    def test_login_success(self, client):
        """Test successful login."""
        response = client.post('/api/auth/login', 
                              json={'username': 'admin', 'password': 'admin123'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert 'user' in data
        assert data['user']['username'] == 'admin'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/api/auth/login', 
                              json={'username': 'wrong', 'password': 'wrong'})
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_profile_success(self, client, auth_headers):
        """Test getting user profile with valid token."""
        response = client.get('/api/auth/profile', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['username'] == 'admin'

class TestDashboard:
    """Test dashboard endpoints."""
    
    def test_get_stats_success(self, client, auth_headers):
        """Test getting dashboard stats."""
        response = client.get('/api/dashboard/stats', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_interactions' in data
        assert 'active_users' in data

class TestEmotions:
    """Test emotions endpoints."""
    
    def test_analyze_emotion_success(self, client, auth_headers):
        """Test emotion analysis with text."""
        response = client.post('/api/emotions/analyze', 
                              headers=auth_headers,
                              json={'text': 'أشعر بالسعادة اليوم'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'emotion' in data
        assert 'confidence' in data

class TestChat:
    """Test chat endpoints."""
    
    def test_send_message_success(self, client, auth_headers):
        """Test sending a message to AI."""
        response = client.post('/api/chat/message', 
                              headers=auth_headers,
                              json={'message': 'مرحباً'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'mood' in data 