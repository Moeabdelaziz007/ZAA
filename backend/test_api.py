import pytest
import json
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
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields."""
        response = client.post('/api/auth/login', json={'username': 'admin'})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_profile_success(self, client, auth_headers):
        """Test getting user profile with valid token."""
        response = client.get('/api/auth/profile', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['username'] == 'admin'
    
    def test_get_profile_no_token(self, client):
        """Test getting profile without token."""
        response = client.get('/api/auth/profile')
        assert response.status_code == 401

class TestDashboard:
    """Test dashboard endpoints."""
    
    def test_get_stats_success(self, client, auth_headers):
        """Test getting dashboard stats."""
        response = client.get('/api/dashboard/stats', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_interactions' in data
        assert 'active_users' in data
        assert 'happiness_level' in data
    
    def test_get_interactions_data(self, client, auth_headers):
        """Test getting interactions data."""
        response = client.get('/api/dashboard/interactions', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_get_activities(self, client, auth_headers):
        """Test getting recent activities."""
        response = client.get('/api/dashboard/activities', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'activities' in data
        assert isinstance(data['activities'], list)

class TestEmotions:
    """Test emotions endpoints."""
    
    def test_get_weekly_emotions(self, client, auth_headers):
        """Test getting weekly emotion data."""
        response = client.get('/api/emotions/weekly', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_analyze_emotion_success(self, client, auth_headers):
        """Test emotion analysis with text."""
        response = client.post('/api/emotions/analyze', 
                              headers=auth_headers,
                              json={'text': 'أشعر بالسعادة اليوم'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'emotion' in data
        assert 'confidence' in data
    
    def test_analyze_emotion_empty_text(self, client, auth_headers):
        """Test emotion analysis with empty text."""
        response = client.post('/api/emotions/analyze', 
                              headers=auth_headers,
                              json={'text': ''})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

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
        assert 'timestamp' in data
    
    def test_send_empty_message(self, client, auth_headers):
        """Test sending empty message."""
        response = client.post('/api/chat/message', 
                              headers=auth_headers,
                              json={'message': ''})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

class TestSkills:
    """Test skills endpoints."""
    
    def test_get_skills(self, client, auth_headers):
        """Test getting skills data."""
        response = client.get('/api/skills', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'skills' in data
        assert 'performance' in data
        assert isinstance(data['skills'], list)
    
    def test_create_sibling_success(self, client, auth_headers):
        """Test creating a digital sibling."""
        response = client.post('/api/skills/create-sibling', 
                              headers=auth_headers,
                              json={'traits': {'specialty': 'programming'}})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'success' in data
        assert 'sibling' in data
        assert data['success'] is True

class TestSettings:
    """Test settings endpoints."""
    
    def test_get_settings(self, client, auth_headers):
        """Test getting system settings."""
        response = client.get('/api/settings', headers=auth_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'settings' in data
        assert isinstance(data['settings'], dict)
    
    def test_update_settings(self, client, auth_headers):
        """Test updating system settings."""
        response = client.post('/api/settings', 
                              headers=auth_headers,
                              json={'theme': 'dark', 'language': 'ar'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'success' in data
        assert data['success'] is True

class TestZeroSystem:
    """Test Zero System integration."""
    
    def test_zero_system_creation(self):
        """Test that Zero System can be created."""
        system = ZeroSystem()
        assert system is not None
        assert len(system.skills) > 0
    
    def test_zero_system_interaction(self):
        """Test Zero System interaction."""
        system = ZeroSystem()
        response = system.interact("مرحباً")
        assert 'output' in response
        assert response['status'] == 'success'
    
    def test_emotion_analysis(self):
        """Test emotion analysis skill."""
        system = ZeroSystem()
        result = system.skills['empathy_sensor'].execute("أشعر بالسعادة")
        assert result['status'] == 'success'
        assert 'empathy' in result

# Integration Tests
class TestAPIIntegration:
    """Integration tests for API endpoints."""
    
    def test_full_user_flow(self, client):
        """Test complete user flow from login to dashboard."""
        # 1. Login
        login_response = client.post('/api/auth/login', 
                                   json={'username': 'admin', 'password': 'admin123'})
        assert login_response.status_code == 200
        token = json.loads(login_response.data)['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # 2. Get profile
        profile_response = client.get('/api/auth/profile', headers=headers)
        assert profile_response.status_code == 200
        
        # 3. Get dashboard stats
        stats_response = client.get('/api/dashboard/stats', headers=headers)
        assert stats_response.status_code == 200
        
        # 4. Send a chat message
        chat_response = client.post('/api/chat/message', 
                                   headers=headers,
                                   json={'message': 'مرحباً'})
        assert chat_response.status_code == 200
        
        # 5. Analyze emotion
        emotion_response = client.post('/api/emotions/analyze', 
                                      headers=headers,
                                      json={'text': 'أشعر بالفرح'})
        assert emotion_response.status_code == 200

# Performance Tests
class TestPerformance:
    """Basic performance tests."""
    
    def test_health_check_response_time(self, client):
        """Test that health check responds quickly."""
        import time
        start_time = time.time()
        response = client.get('/api/health')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond in less than 1 second
    
    def test_multiple_concurrent_requests(self, client, auth_headers):
        """Test handling multiple requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get('/api/dashboard/stats', headers=auth_headers)
            results.append(response.status_code)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5

if __name__ == '__main__':
    pytest.main([__file__]) 