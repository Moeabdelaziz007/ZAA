"""
User preference service.
This module contains the user preference service class and related functions.
"""

from typing import Any, List, Optional
from sqlalchemy.orm import Session

from models.preference import UserPreference
from schemas.preference import PreferenceCreate, PreferenceUpdate
from services.base import BaseService

class PreferenceService(BaseService[UserPreference, PreferenceCreate, PreferenceUpdate]):
    """User preference service class."""
    
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserPreference]:
        """Get preferences by user."""
        return (
            db.query(self.model)
            .filter(UserPreference.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_category(
        self,
        db: Session,
        *,
        user_id: int,
        category: str
    ) -> Optional[UserPreference]:
        """Get user preference for a specific category."""
        return (
            db.query(self.model)
            .filter(
                UserPreference.user_id == user_id,
                UserPreference.category == category
            )
            .first()
        )
    
    def update_or_create(
        self,
        db: Session,
        *,
        user_id: int,
        category: str,
        obj_in: PreferenceCreate
    ) -> UserPreference:
        """Update or create user preference."""
        preference = self.get_by_category(db, user_id=user_id, category=category)
        if preference:
            return self.update(db, db_obj=preference, obj_in=obj_in)
        return self.create_with_user(db, obj_in=obj_in, user_id=user_id)
    
    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: PreferenceCreate,
        user_id: int
    ) -> UserPreference:
        """Create new preference with user."""
        obj_in_data = obj_in.dict()
        db_obj = UserPreference(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_user_categories(
        self,
        db: Session,
        *,
        user_id: int
    ) -> List[str]:
        """Get all categories for a user."""
        preferences = self.get_by_user(db, user_id=user_id)
        return [p.category for p in preferences]
    
    def get_user_tags(
        self,
        db: Session,
        *,
        user_id: int
    ) -> List[str]:
        """Get all tags for a user."""
        preferences = self.get_by_user(db, user_id=user_id)
        tags = []
        for p in preferences:
            tags.extend(p.tags)
        return list(set(tags))

preference_service = PreferenceService(UserPreference) 