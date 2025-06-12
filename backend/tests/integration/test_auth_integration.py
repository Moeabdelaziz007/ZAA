"""
Authentication integration tests.
Tests the authentication system and security features.

Arabic:
اختبارات تكامل المصادقة.
تختبر نظام المصادقة وميزات الأمان.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from core.database import get_db
from api.models.user import User
from core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    ALGORITHM,
    SECRET_KEY
)

@pytest.fixture
def client():
    """Create a test client."""
    from api.main import app
    return TestClient(app)

@pytest.fixture
def db_session():
    """Create a test database session."""
    from core.database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def test_user(db_session: Session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password123"),
        full_name="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_password_hashing():
    """Test password hashing and verification."""
    password = "test_password"
    hashed = get_password_hash(password)
    
    # Test correct password
    assert verify_password(password, hashed)
    
    # Test incorrect password
    assert not verify_password("wrong_password", hashed)
    
    # Test different hashes for same password
    hashed2 = get_password_hash(password)
    assert hashed != hashed2

def test_jwt_token_creation():
    """Test JWT token creation and validation."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    # Decode token
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == data["sub"]
    
    # Test token expiration
    expired_token = jwt.encode(
        {
            "sub": data["sub"],
            "exp": datetime.utcnow() - timedelta(minutes=1)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(expired_token, SECRET_KEY, algorithms=[ALGORITHM])

def test_authentication_flow(client: TestClient, test_user: User):
    """Test the complete authentication flow."""
    # Test login with correct credentials
    login_data = {
        "username": test_user.email,
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    # Test login with incorrect password
    login_data["password"] = "wrong_password"
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    
    # Test login with non-existent user
    login_data["username"] = "nonexistent@example.com"
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401

def test_protected_endpoints(client: TestClient, test_user: User):
    """Test access to protected endpoints."""
    # Create valid token
    token = create_access_token({"sub": test_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test access with valid token
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    
    # Test access without token
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    
    # Test access with invalid token
    headers["Authorization"] = "Bearer invalid_token"
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401

def test_password_change(client: TestClient, test_user: User):
    """Test password change functionality."""
    # Create valid token
    token = create_access_token({"sub": test_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test password change
    password_data = {
        "current_password": "password123",
        "new_password": "new_password123"
    }
    response = client.post("/api/v1/auth/change-password", headers=headers, json=password_data)
    assert response.status_code == 200
    
    # Test login with new password
    login_data = {
        "username": test_user.email,
        "password": "new_password123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json() 