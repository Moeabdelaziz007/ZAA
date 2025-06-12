"""
Cache integration tests.
Tests the caching functionality and performance.

Arabic:
اختبارات تكامل التخزين المؤقت.
تختبر وظائف وأداء التخزين المؤقت.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import time
import redis

from core.database import get_db
from api.models.user import User
from api.models.item import Item
from core.security import create_access_token
from core.cache import get_redis_client

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
def redis_client():
    """Create a Redis client."""
    client = get_redis_client()
    yield client
    client.flushdb()  # Clean up after tests

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

def test_redis_connection(redis_client: redis.Redis):
    """Test Redis connection."""
    # Test basic operations
    redis_client.set("test_key", "test_value")
    assert redis_client.get("test_key") == b"test_value"
    
    # Test expiration
    redis_client.setex("expiring_key", 1, "expiring_value")
    assert redis_client.get("expiring_key") == b"expiring_value"
    time.sleep(2)
    assert redis_client.get("expiring_key") is None

def test_api_response_caching(client: TestClient, test_item: Item):
    """Test API response caching."""
    # First request (cache miss)
    start_time = time.time()
    response1 = client.get(f"/api/v1/items/{test_item.id}")
    first_request_time = time.time() - start_time
    
    # Second request (cache hit)
    start_time = time.time()
    response2 = client.get(f"/api/v1/items/{test_item.id}")
    second_request_time = time.time() - start_time
    
    assert second_request_time < first_request_time
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json() == response2.json()

def test_cache_invalidation(client: TestClient, test_item: Item):
    """Test cache invalidation."""
    # Get initial response
    response1 = client.get(f"/api/v1/items/{test_item.id}")
    assert response1.status_code == 200
    
    # Update item
    update_data = {"title": "Updated Title"}
    response = client.put(f"/api/v1/items/{test_item.id}", json=update_data)
    assert response.status_code == 200
    
    # Get updated response
    response2 = client.get(f"/api/v1/items/{test_item.id}")
    assert response2.status_code == 200
    assert response2.json()["title"] == "Updated Title"

def test_cache_headers(client: TestClient, test_item: Item):
    """Test cache control headers."""
    response = client.get(f"/api/v1/items/{test_item.id}")
    
    assert "cache-control" in response.headers
    assert "etag" in response.headers
    assert "last-modified" in response.headers

def test_cache_stale_while_revalidate(client: TestClient, test_item: Item):
    """Test stale-while-revalidate caching strategy."""
    # First request
    response1 = client.get(f"/api/v1/items/{test_item.id}")
    etag = response1.headers["etag"]
    
    # Request with stale cache
    headers = {"If-None-Match": etag}
    response2 = client.get(f"/api/v1/items/{test_item.id}", headers=headers)
    assert response2.status_code == 304

def test_cache_batch_operations(redis_client: redis.Redis):
    """Test batch cache operations."""
    # Test pipeline
    with redis_client.pipeline() as pipe:
        for i in range(10):
            pipe.set(f"key{i}", f"value{i}")
        pipe.execute()
    
    # Verify all values
    for i in range(10):
        assert redis_client.get(f"key{i}") == f"value{i}".encode()

def test_cache_pattern_matching(redis_client: redis.Redis):
    """Test cache pattern matching."""
    # Set multiple keys with pattern
    for i in range(5):
        redis_client.set(f"user:{i}:profile", f"profile{i}")
        redis_client.set(f"user:{i}:settings", f"settings{i}")
    
    # Get all profile keys
    profile_keys = redis_client.keys("user:*:profile")
    assert len(profile_keys) == 5
    
    # Delete all user keys
    redis_client.delete(*redis_client.keys("user:*"))
    assert len(redis_client.keys("user:*")) == 0

def test_cache_compression(redis_client: redis.Redis):
    """Test cache compression."""
    # Large data
    large_data = "x" * 1000
    
    # Set with compression
    redis_client.set("compressed", large_data)
    
    # Verify compression
    assert len(redis_client.get("compressed")) < len(large_data.encode())

def test_cache_error_handling(redis_client: redis.Redis):
    """Test cache error handling."""
    # Test connection error
    redis_client.connection_pool.disconnect()
    with pytest.raises(redis.ConnectionError):
        redis_client.get("test_key")
    
    # Test invalid key
    with pytest.raises(redis.RedisError):
        redis_client.get(None) 