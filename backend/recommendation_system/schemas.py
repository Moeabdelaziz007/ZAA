from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime

class UserInteractionCreate(BaseModel):
    user_id: int
    item_id: int
    interaction_type: str = Field(..., description="نوع التفاعل (view, like, share, purchase)")
    interaction_value: float = Field(..., description="قيمة التفاعل (مثال: التقييم)")
    context: Optional[Dict] = Field(default={}, description="سياق إضافي للتفاعل")

class RecommendationResponse(BaseModel):
    item_id: int
    score: float
    algorithm: str
    metadata: Optional[Dict] = None

class UserPreferencesUpdate(BaseModel):
    categories: Optional[List[str]] = Field(default=[], description="الفئات المفضلة")
    interests: Optional[List[str]] = Field(default=[], description="الاهتمامات")
    preferences: Optional[Dict] = Field(default={}, description="تفضيلات إضافية")

class ItemFeatures(BaseModel):
    title: str
    description: str
    category: str
    features: Dict
    metadata: Optional[Dict] = None

class UserBehavior(BaseModel):
    total_interactions: int
    interaction_types: Dict[str, int]
    categories: Dict[str, int]
    time_distribution: Dict[str, int]

class SimilarItem(BaseModel):
    item_id: int
    title: str
    similarity_score: float 