"""
Item service.
This module contains the item service class and related functions.
"""

from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from models.item import Item
from schemas.item import ItemCreate, ItemUpdate
from services.base import BaseService

class ItemService(BaseService[Item, ItemCreate, ItemUpdate]):
    """Item service class."""
    
    def create_with_owner(
        self,
        db: Session,
        *,
        obj_in: ItemCreate,
        owner_id: int
    ) -> Item:
        """Create new item with owner."""
        obj_in_data = obj_in.dict()
        db_obj = Item(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> list[Item]:
        """Get items by owner."""
        return (
            db.query(self.model)
            .filter(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_category(
        self,
        db: Session,
        *,
        category: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[Item]:
        """Get items by category."""
        return (
            db.query(self.model)
            .filter(Item.category == category)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> list[Item]:
        """Search items by title or description."""
        return (
            db.query(self.model)
            .filter(
                (Item.title.ilike(f"%{query}%")) |
                (Item.description.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

item_service = ItemService(Item) 