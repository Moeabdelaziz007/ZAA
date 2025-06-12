"""
Recommendation endpoints.
This module contains the recommendation-related API endpoints.
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from redis import Redis
from datetime import timedelta

from core.database import get_db
from core.redis import get_redis
from core.security import get_current_user
from core.rate_limit import rate_limit
from ..models.user import User
from schemas.recommendation import RecommendationResponse
from ..services.recommendation import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()

@router.get("/{user_id}", response_model=List[RecommendationResponse])
@rate_limit(times=100, period=3600)  # 100 requests per hour
async def get_recommendations(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized recommendations for the current user.
    
    - **user_id**: ID of the user
    - **limit**: Number of recommendations to return (maximum 50)
    """
    # Check permissions
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to access these recommendations")
    
    # Try getting from cache
    cache_key = f"recommendations:{user_id}:{limit}"
    cached_recommendations = redis.get(cache_key)
    
    if cached_recommendations:
        return cached_recommendations
    
    # Get from database
    service = RecommendationService(db)
    recommendations = await service.get_recommendations(user_id, limit)
    
    # Store in cache for 1 hour
    redis.setex(
        cache_key,
        timedelta(hours=1),
        recommendations
    )
    
    return recommendations

@router.post("/train")
async def train_model(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Train the recommendation model in the background
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to train the model")
    
    service = RecommendationService(db)
    background_tasks.add_task(service.train_model)
    
    return {"message": "Model training started in the background"}

@router.get("/similar/{item_id}", response_model=List[RecommendationResponse])
@rate_limit(times=200, period=3600)  # 200 requests per hour
async def get_similar_items(
    item_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    """
    Get similar items
    
    - **item_id**: ID of the item
    - **limit**: Number of items to return (maximum 50)
    """
    # Try getting from cache
    cache_key = f"similar_items:{item_id}:{limit}"
    cached_items = redis.get(cache_key)
    
    if cached_items:
        return cached_items
    
    # Get from database
    service = RecommendationService(db)
    similar_items = await service.get_similar_items(item_id, limit)
    
    # Store in cache for 30 minutes
    redis.setex(
        cache_key,
        timedelta(minutes=30),
        similar_items
    )
    
    return similar_items

@router.get("/trending", response_model=List[RecommendationResponse])
async def get_trending_items(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get trending items.
    """
    recommendations = recommendation_service.get_trending_items(
        db=db,
        skip=skip,
        limit=limit
    )
    return recommendations

@router.get("/category/{category}", response_model=List[RecommendationResponse])
async def get_category_recommendations(
    *,
    db: Session = Depends(get_db),
    category: str,
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get recommendations for a specific category.
    """
    recommendations = recommendation_service.get_category_recommendations(
        db=db,
        category=category,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return recommendations 