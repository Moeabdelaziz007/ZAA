"""
Performance integration tests.
Tests the performance and scalability of the application.

Arabic:
اختبارات تكامل الأداء.
تختبر أداء وقابلية تطوير التطبيق.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import time
from concurrent.futures import ThreadPoolExecutor

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
def test_users(db_session: Session):
    """Create multiple test users."""
    users = []
    for i in range(10):
        user = User(
            email=f"test{i}@example.com",
            hashed_password="hashed_password",
            full_name=f"Test User {i}",
            is_active=True
        )
        db_session.add(user)
    db_session.commit()
    return users

@pytest.fixture
def test_items(db_session: Session, test_users: list[User]):
    """Create multiple test items."""
    items = []
    for i in range(50):
        item = Item(
            title=f"Test Item {i}",
            description=f"Test Description {i}",
            price=99.99 + i,
            category=f"Category {i % 5}",
            owner_id=test_users[i % len(test_users)].id
        )
        db_session.add(item)
    db_session.commit()
    return items

def test_database_query_performance(db_session: Session, test_items: list[Item]):
    """Test database query performance."""
    # Test simple query
    start_time = time.time()
    items = db_session.query(Item).all()
    simple_query_time = time.time() - start_time
    assert simple_query_time < 0.1  # Should be less than 100ms
    
    # Test filtered query
    start_time = time.time()
    filtered_items = db_session.query(Item).filter(
        Item.category == "Category 0"
    ).all()
    filtered_query_time = time.time() - start_time
    assert filtered_query_time < 0.1  # Should be less than 100ms
    
    # Test pagination
    start_time = time.time()
    paginated_items = db_session.query(Item).offset(0).limit(10).all()
    pagination_time = time.time() - start_time
    assert pagination_time < 0.1  # Should be less than 100ms

def test_api_response_time(client: TestClient, test_items: list[Item]):
    """Test API endpoint response times."""
    # Test items endpoint
    start_time = time.time()
    response = client.get("/api/v1/items/")
    items_time = time.time() - start_time
    assert items_time < 0.2  # Should be less than 200ms
    assert response.status_code == 200
    
    # Test single item endpoint
    start_time = time.time()
    response = client.get(f"/api/v1/items/{test_items[0].id}")
    single_item_time = time.time() - start_time
    assert single_item_time < 0.1  # Should be less than 100ms
    assert response.status_code == 200

def test_concurrent_requests(client: TestClient, test_items: list[Item]):
    """Test handling of concurrent requests."""
    def make_request(item_id: int):
        return client.get(f"/api/v1/items/{item_id}")
    
    # Test concurrent requests
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(make_request, item.id)
            for item in test_items[:10]
        ]
        responses = [f.result() for f in futures]
    concurrent_time = time.time() - start_time
    
    assert concurrent_time < 1.0  # Should handle 10 concurrent requests in under 1 second
    assert all(r.status_code == 200 for r in responses)

def test_bulk_operations_performance(db_session: Session):
    """Test bulk operations performance."""
    # Test bulk insert
    start_time = time.time()
    items = [
        Item(
            title=f"Bulk Item {i}",
            description=f"Bulk Description {i}",
            price=99.99,
            category="Bulk Category"
        )
        for i in range(100)
    ]
    db_session.bulk_save_objects(items)
    db_session.commit()
    bulk_insert_time = time.time() - start_time
    assert bulk_insert_time < 0.5  # Should insert 100 items in under 500ms
    
    # Test bulk update
    start_time = time.time()
    db_session.query(Item).filter(
        Item.category == "Bulk Category"
    ).update({"price": 149.99})
    db_session.commit()
    bulk_update_time = time.time() - start_time
    assert bulk_update_time < 0.2  # Should update 100 items in under 200ms 
