"""
API integration tests.
Tests the complete request-response cycle for all API endpoints.

Arabic:
اختبارات تكامل API.
تختبر دورة الطلب-الاستجابة الكاملة لجميع نقاط نهاية API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from models.item import Item
from core.security import create_access_token

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

@pytest.fixture
def test_item(db_session: Session, test_user: User):
    """Create a test item."""
    item = Item(
        title="Test Item",
        description="Test Description",
        price=99.99,
        category="Test Category",
        owner_id=test_user.id
    )
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item

@pytest.fixture
def test_token(test_user: User):
    """Create a test access token."""
    return create_access_token({"sub": test_user.email})

def test_auth_endpoints(client: TestClient, test_user: User):
    """Test authentication endpoints."""
    # Test login
    login_data = {
        "username": test_user.email,
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    # Test register
    register_data = {
        "email": "new@example.com",
        "password": "password123",
        "full_name": "New User"
    }
    response = client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == 200
    assert response.json()["email"] == register_data["email"]

def test_user_endpoints(client: TestClient, test_token: str, test_user: User):
    """Test user endpoints."""
    headers = {"Authorization": f"Bearer {test_token}"}
    
    # Test get current user
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user.email
    
    # Test update user
    update_data = {"full_name": "Updated Name"}
    response = client.put("/api/v1/users/me", headers=headers, json=update_data)
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"

def test_item_endpoints(
    client: TestClient,
    test_token: str,
    test_user: User,
    test_item: Item
):
    """Test item endpoints."""
    headers = {"Authorization": f"Bearer {test_token}"}
    
    # Test create item
    item_data = {
        "title": "New Item",
        "description": "New Description",
        "price": 149.99,
        "category": "New Category"
    }
    response = client.post("/api/v1/items/", headers=headers, json=item_data)
    assert response.status_code == 200
    assert response.json()["title"] == item_data["title"]
    
    # Test get items
    response = client.get("/api/v1/items/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    # Test get item
    response = client.get(f"/api/v1/items/{test_item.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == test_item.id

def test_recommendation_endpoints(
    client: TestClient,
    test_token: str,
    test_user: User,
    test_item: Item
):
    """Test recommendation endpoints."""
    headers = {"Authorization": f"Bearer {test_token}"}
    
    # Test get recommendations
    response = client.get("/api/v1/recommendations/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Test get similar items
    response = client.get(
        f"/api/v1/recommendations/similar/{test_item.id}",
        headers=headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
    # Test get trending items
    response = client.get("/api/v1/recommendations/trending", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_interaction_endpoints(
    client: TestClient,
    test_token: str,
    test_user: User,
    test_item: Item
):
    """Test interaction endpoints."""
    headers = {"Authorization": f"Bearer {test_token}"}
    
    # Test create interaction
    interaction_data = {
        "item_id": test_item.id,
        "interaction_type": "view",
        "rating": 4.5
    }
    response = client.post(
        "/api/v1/interactions/",
        headers=headers,
        json=interaction_data
    )
    assert response.status_code == 200
    assert response.json()["interaction_type"] == "view"
    
    # Test get user interactions
    response = client.get("/api/v1/interactions/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_preference_endpoints(
    client: TestClient,
    test_token: str,
    test_user: User
):
    """Test preference endpoints."""
    headers = {"Authorization": f"Bearer {test_token}"}
    
    # Test create preference
    preference_data = {
        "category": "Electronics",
        "weight": 0.8,
        "tags": ["gadgets", "tech"]
    }
    response = client.post(
        "/api/v1/preferences/",
        headers=headers,
        json=preference_data
    )
    assert response.status_code == 200
    assert response.json()["category"] == "Electronics"
    
    # Test get user preferences
    response = client.get("/api/v1/preferences/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0 