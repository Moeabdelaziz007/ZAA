"""
Validation integration tests.
Tests input validation and data integrity.

Arabic:
اختبارات تكامل التحقق من الصحة.
تختبر التحقق من صحة المدخلات وسلامة البيانات.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.database import get_db
from models.user import User
from models.item import Item
from core.security import create_access_token
from schemas.user import UserCreate, UserUpdate
from schemas.item import ItemCreate, ItemUpdate

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

def test_user_validation():
    """Test user data validation."""
    # Test valid user data
    valid_data = {
        "email": "valid@example.com",
        "password": "valid_password123",
        "full_name": "Valid User"
    }
    user = UserCreate(**valid_data)
    assert user.email == valid_data["email"]
    assert user.full_name == valid_data["full_name"]
    
    # Test invalid email
    with pytest.raises(ValueError):
        UserCreate(
            email="invalid_email",
            password="password123",
            full_name="Test User"
        )
    
    # Test short password
    with pytest.raises(ValueError):
        UserCreate(
            email="test@example.com",
            password="short",
            full_name="Test User"
        )

def test_item_validation():
    """Test item data validation."""
    # Test valid item data
    valid_data = {
        "title": "Valid Item",
        "description": "Valid Description",
        "price": 99.99,
        "category": "Valid Category"
    }
    item = ItemCreate(**valid_data)
    assert item.title == valid_data["title"]
    assert item.price == valid_data["price"]
    
    # Test negative price
    with pytest.raises(ValueError):
        ItemCreate(
            title="Test Item",
            description="Test Description",
            price=-10.0,
            category="Test Category"
        )
    
    # Test empty title
    with pytest.raises(ValueError):
        ItemCreate(
            title="",
            description="Test Description",
            price=99.99,
            category="Test Category"
        )

def test_api_input_validation(client: TestClient, test_user: User):
    """Test API input validation."""
    # Create valid token
    token = create_access_token({"sub": test_user.email})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test invalid user update
    invalid_data = {
        "email": "invalid_email",
        "full_name": ""  # Empty name
    }
    response = client.put("/api/v1/users/me", headers=headers, json=invalid_data)
    assert response.status_code == 422
    
    # Test invalid item creation
    invalid_item = {
        "title": "",  # Empty title
        "description": "Test Description",
        "price": -10.0,  # Negative price
        "category": "Test Category"
    }
    response = client.post("/api/v1/items/", headers=headers, json=invalid_item)
    assert response.status_code == 422

def test_unique_constraint_validation(db_session: Session):
    """Test unique constraint validation."""
    # Create first user
    user1 = User(
        email="unique@example.com",
        hashed_password="hashed_password",
        full_name="First User"
    )
    db_session.add(user1)
    db_session.commit()
    
    # Try to create second user with same email
    user2 = User(
        email="unique@example.com",
        hashed_password="hashed_password",
        full_name="Second User"
    )
    with pytest.raises(Exception):
        db_session.add(user2)
        db_session.commit()

def test_foreign_key_validation(db_session: Session):
    """Test foreign key constraint validation."""
    # Try to create item with non-existent user
    item = Item(
        title="Test Item",
        description="Test Description",
        price=99.99,
        category="Test Category",
        owner_id=999  # Non-existent user ID
    )
    with pytest.raises(Exception):
        db_session.add(item)
        db_session.commit() 
