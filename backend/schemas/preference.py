"""
User preference schemas.
This module contains Pydantic models for user preference-related operations.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class PreferenceBase(BaseModel):
    """Base preference schema."""
    category: str
    weight: float
    tags: List[str] = []

class PreferenceCreate(PreferenceBase):
    """Preference creation schema."""
    pass

class PreferenceUpdate(PreferenceBase):
    """Preference update schema."""
    category: Optional[str] = None
    weight: Optional[float] = None
    tags: Optional[List[str]] = None

class PreferenceInDBBase(PreferenceBase):
    """Base preference in database schema."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PreferenceResponse(PreferenceInDBBase):
    """Preference response schema."""
    pass

class PreferenceInDB(PreferenceInDBBase):
    """Preference in database schema."""
    pass 