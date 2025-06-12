"""
Services integration tests.
Tests the interaction between different services.

Arabic:
اختبارات تكامل الخدمات.
تختبر التفاعل بين الخدمات المختلفة.
"""

import pytest
from sqlalchemy.orm import Session
from datetime import datetime

from core.database import get_db
from models.user import User
from models.item import Item
from models.interaction import Interaction
from models.preference import UserPreference
from services.user import UserService
from services.item import ItemService
from services.interaction import InteractionService
from services.preference import PreferenceService
from services.recommendation import RecommendationService

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

def test_user_service_integration(db_session: Session):
    """Test UserService integration."""
    user_service = UserService()
    
    # Create user
    user_data = {
        "email": "new@example.com",
        "password": "password123",
        "full_name": "New User"
    }
    user = user_service.create(db_session, obj_in=user_data)
    assert user.email == user_data["email"]
    
    # Get user
    retrieved_user = user_service.get(db_session, id=user.id)
    assert retrieved_user.id == user.id
    
    # Update user
    update_data = {"full_name": "Updated Name"}
    updated_user = user_service.update(db_session, db_obj=user, obj_in=update_data)
    assert updated_user.full_name == "Updated Name"

def test_item_service_integration(db_session: Session, test_user: User):
    """Test ItemService integration."""
    item_service = ItemService()
    
    # Create item
    item_data = {
        "title": "New Item",
        "description": "New Description",
        "price": 149.99,
        "category": "New Category"
    }
    item = item_service.create_with_owner(db_session, obj_in=item_data, owner_id=test_user.id)
    assert item.title == item_data["title"]
    
    # Get items by owner
    items = item_service.get_by_owner(db_session, owner_id=test_user.id)
    assert len(items) > 0
    
    # Search items
    search_results = item_service.search(db_session, query="New")
    assert len(search_results) > 0

def test_interaction_service_integration(db_session: Session, test_user: User, test_item: Item):
    """Test InteractionService integration."""
    interaction_service = InteractionService()
    
    # Create interaction
    interaction_data = {
        "item_id": test_item.id,
        "interaction_type": "view",
        "rating": 4.5
    }
    interaction = interaction_service.create_with_user(
        db_session,
        obj_in=interaction_data,
        user_id=test_user.id
    )
    assert interaction.interaction_type == "view"
    
    # Get user interactions
    interactions = interaction_service.get_by_user(db_session, user_id=test_user.id)
    assert len(interactions) > 0
    
    # Get average rating
    avg_rating = interaction_service.get_average_rating(db_session, item_id=test_item.id)
    assert avg_rating == 4.5

def test_preference_service_integration(db_session: Session, test_user: User):
    """Test PreferenceService integration."""
    preference_service = PreferenceService()
    
    # Create preference
    preference_data = {
        "category": "Electronics",
        "weight": 0.8,
        "tags": ["gadgets", "tech"]
    }
    preference = preference_service.create_with_user(
        db_session,
        obj_in=preference_data,
        user_id=test_user.id
    )
    assert preference.category == "Electronics"
    
    # Get user preferences
    preferences = preference_service.get_by_user(db_session, user_id=test_user.id)
    assert len(preferences) > 0
    
    # Get user categories
    categories = preference_service.get_user_categories(db_session, user_id=test_user.id)
    assert "Electronics" in categories

def test_recommendation_service_integration(
    db_session: Session,
    test_user: User,
    test_item: Item
):
    """Test RecommendationService integration."""
    recommendation_service = RecommendationService()
    
    # Get recommendations
    recommendations = recommendation_service.get_recommendations(
        db_session,
        user_id=test_user.id
    )
    assert isinstance(recommendations, list)
    
    # Get similar items
    similar_items = recommendation_service.get_similar_items(
        db_session,
        item_id=test_item.id
    )
    assert isinstance(similar_items, list)
    
    # Get trending items
    trending_items = recommendation_service.get_trending_items(db_session)
    assert isinstance(trending_items, list) 