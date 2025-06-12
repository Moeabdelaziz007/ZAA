"""
Base service class with common functionality.
This module provides a base class for all services with shared methods.
"""

from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseService(Generic[ModelType]):
    """
    Base class for all services with common CRUD operations.
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Get all records with pagination."""
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: dict) -> ModelType:
        """Create a new record."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: dict
    ) -> ModelType:
        """Update an existing record."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> Optional[ModelType]:
        """Delete a record by ID."""
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def exists(self, db: Session, id: int) -> bool:
        """Check if a record exists."""
        return db.query(self.model).filter(self.model.id == id).first() is not None
    
    def count(self, db: Session) -> int:
        """Get total count of records."""
        return db.query(self.model).count() 