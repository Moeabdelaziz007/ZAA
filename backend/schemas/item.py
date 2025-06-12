"""
Item schemas.
This module contains Pydantic models for item-related operations.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, constr

class ItemBase(BaseModel):
    """Base item schema."""
    title: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category: str
    tags: list[str] = []

class ItemCreate(ItemBase):
    """Item creation schema."""
    pass

class ItemUpdate(ItemBase):
    """Item update schema."""
    title: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None

class ItemInDBBase(ItemBase):
    """Base item in database schema."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ItemResponse(ItemInDBBase):
    """Item response schema."""
    pass

class ItemInDB(ItemInDBBase):
    """Item in database schema."""
    pass 