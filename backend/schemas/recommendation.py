"""
Recommendation schemas.
This module contains Pydantic models for recommendation-related operations.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class RecommendationBase(BaseModel):
    """Base recommendation schema."""
    item_id: int
    score: float
    reason: Optional[str] = None

class RecommendationCreate(RecommendationBase):
    """Recommendation creation schema."""
    pass

class RecommendationUpdate(RecommendationBase):
    """Recommendation update schema."""
    score: Optional[float] = None
    reason: Optional[str] = None

class RecommendationInDBBase(RecommendationBase):
    """Base recommendation in database schema."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RecommendationResponse(RecommendationInDBBase):
    """Recommendation response schema."""
    pass

class RecommendationInDB(RecommendationInDBBase):
    """Recommendation in database schema."""
    pass 