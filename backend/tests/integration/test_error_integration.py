"""
Error handling integration tests.
Tests error handling and recovery mechanisms.

Arabic:
اختبارات تكامل معالجة الأخطاء.
تختبر آليات معالجة الأخطاء والتعافي.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import redis.exceptions

from core.database import get_db
from api.models.user import User
from api.models.item import Item
from core.security import create_access_token
from core.exceptions import (
    DatabaseError,
    CacheError,
    ValidationError,
    AuthenticationError,
    NotFoundError
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
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

def test_database_error_handling(db_session: Session):
    """Test database error handling."""
    # Test connection error
    db_session.connection().close()
    with pytest.raises(DatabaseError):
        db_session.query(User).all()
    
    # Test transaction error
    with pytest.raises(DatabaseError):
        with db_session.begin():
            user = User(
                email="test@example.com",
                hashed_password="hashed_password",
                full_name="Test User"
            )
            db_session.add(user)
            db_session.add(user)  # Duplicate key error

def test_cache_error_handling(redis_client):
    """Test cache error handling."""
    # Test connection error
    redis_client.connection_pool.disconnect()
    with pytest.raises(CacheError):
        redis_client.get("test_key")
    
    # Test invalid key
    with pytest.raises(CacheError):
        redis_client.get(None)

def test_validation_error_handling(client: TestClient, test_user: User):
    """Test validation error handling."""
    # Create valid token
    token = create_access_token({"sub": test_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test invalid input
    invalid_data = {
        "email": "invalid_email",
        "full_name": ""  # Empty name
    }
    response = client.put("/api/v1/users/me", headers=headers, json=invalid_data)
    assert response.status_code == 422
    assert "validation_error" in response.json()

def test_authentication_error_handling(client: TestClient):
    """Test authentication error handling."""
    # Test invalid token
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401
    assert "authentication_error" in response.json()
    
    # Test expired token
    expired_token = create_access_token(
        {"sub": "test@example.com"},
        expires_delta=timedelta(microseconds=1)
    )
    time.sleep(0.1)
    headers = {"Authorization": f"Bearer {expired_token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401
    assert "token_expired" in response.json()

def test_not_found_error_handling(client: TestClient, test_user: User):
    """Test not found error handling."""
    # Create valid token
    token = create_access_token({"sub": test_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test non-existent item
    response = client.get("/api/v1/items/999", headers=headers)
    assert response.status_code == 404
    assert "not_found" in response.json()
    
    # Test non-existent user
    response = client.get("/api/v1/users/999", headers=headers)
    assert response.status_code == 404
    assert "not_found" in response.json()

def test_rate_limit_error_handling(client: TestClient):
    """Test rate limit error handling."""
    # Make multiple requests
    for _ in range(10):
        response = client.get("/api/v1/items/")
        assert response.status_code == 200
    
    # Test rate limit exceeded
    response = client.get("/api/v1/items/")
    assert response.status_code == 429
    assert "rate_limit_exceeded" in response.json()

def test_internal_server_error_handling(client: TestClient, test_user: User):
    """Test internal server error handling."""
    # Create valid token
    token = create_access_token({"sub": test_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test database connection error
    db_session.connection().close()
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 500
    assert "internal_server_error" in response.json()

def test_error_logging(client: TestClient, caplog):
    """Test error logging."""
    # Test error logging
    with caplog.at_level(logging.ERROR):
        response = client.get("/api/v1/non-existent-endpoint")
        assert response.status_code == 404
        assert "ERROR" in caplog.text
        assert "non-existent-endpoint" in caplog.text

def test_error_recovery(client: TestClient, test_user: User):
    """Test error recovery."""
    # Create valid token
    token = create_access_token({"sub": test_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test retry mechanism
    for _ in range(3):
        try:
            response = client.get("/api/v1/users/me", headers=headers)
            if response.status_code == 200:
                break
        except Exception:
            continue
    else:
        pytest.fail("Failed to recover from error after retries")

def test_error_response_format(client: TestClient):
    """Test error response format."""
    # Test 404 error
    response = client.get("/api/v1/non-existent-endpoint")
    assert response.status_code == 404
    error_data = response.json()
    assert "error" in error_data
    assert "message" in error_data
    assert "code" in error_data
    
    # Test 422 error
    response = client.post("/api/v1/users/", json={})
    assert response.status_code == 422
    error_data = response.json()
    assert "error" in error_data
    assert "message" in error_data
    assert "code" in error_data 