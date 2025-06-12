import pytest
from fastapi.testclient import TestClient
from ..core.auth import create_access_token, verify_password
from ..models.user import User
from ..main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return User(
        username="testuser",
        email="test@example.com",
        hashed_password=verify_password("testpass123"),
        full_name="Test User"
    )

@pytest.fixture
def test_token(test_user):
    return create_access_token({"sub": test_user.username})

def test_login_success(test_user):
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == test_user.username

def test_login_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        json={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_get_profile(test_token):
    response = client.get(
        "/api/auth/profile",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["username"] == "testuser"

def test_get_profile_unauthorized():
    response = client.get("/api/auth/profile")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated" 