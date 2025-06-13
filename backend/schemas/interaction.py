"""Interaction schemas.
This module contains Pydantic models for interaction-related operations."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class InteractionBase(BaseModel):
    item_id: int
    interaction_type: str
    rating: Optional[float] = None
    comment: Optional[str] = None

class InteractionCreate(InteractionBase):
    """Schema for creating an interaction."""
    pass

class InteractionUpdate(InteractionBase):
    """Schema for updating an interaction."""
    item_id: Optional[int] = None
    interaction_type: Optional[str] = None

class InteractionInDBBase(InteractionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class InteractionResponse(InteractionInDBBase):
    """Schema returned in API responses."""
    pass

class InteractionInDB(InteractionInDBBase):
    """Internal schema with database-specific fields."""
    pass
