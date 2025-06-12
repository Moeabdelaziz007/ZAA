"""
Interaction service.
This module contains the interaction service class and related functions.
"""

from typing import Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.interaction import Interaction
from schemas.interaction import InteractionCreate
from services.base import BaseService

class InteractionService(BaseService[Interaction, InteractionCreate, Any]):
    """Interaction service class."""
    
    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: InteractionCreate,
        user_id: int
    ) -> Interaction:
        """Create new interaction with user."""
        obj_in_data = obj_in.dict()
        db_obj = Interaction(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Interaction]:
        """Get interactions by user."""
        return (
            db.query(self.model)
            .filter(Interaction.user_id == user_id)
            .order_by(desc(Interaction.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_item(
        self,
        db: Session,
        *,
        item_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Interaction]:
        """Get interactions by item."""
        return (
            db.query(self.model)
            .filter(Interaction.item_id == item_id)
            .order_by(desc(Interaction.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_type(
        self,
        db: Session,
        *,
        interaction_type: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Interaction]:
        """Get interactions by type."""
        return (
            db.query(self.model)
            .filter(Interaction.interaction_type == interaction_type)
            .order_by(desc(Interaction.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_user_item_interaction(
        self,
        db: Session,
        *,
        user_id: int,
        item_id: int
    ) -> Optional[Interaction]:
        """Get specific user-item interaction."""
        return (
            db.query(self.model)
            .filter(
                Interaction.user_id == user_id,
                Interaction.item_id == item_id
            )
            .first()
        )
    
    def get_average_rating(
        self,
        db: Session,
        *,
        item_id: int
    ) -> float:
        """Get average rating for an item."""
        result = (
            db.query(self.model)
            .filter(
                Interaction.item_id == item_id,
                Interaction.rating.isnot(None)
            )
            .with_entities(func.avg(Interaction.rating))
            .scalar()
        )
        return result or 0.0

interaction_service = InteractionService(Interaction) 