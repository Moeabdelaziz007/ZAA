"""
User preference endpoints.
This module contains the user preference-related API endpoints.
"""

from typing import Any, List, BackgroundTasks
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from redis import Redis
from datetime import timedelta

from core.database import get_db
from core.redis import get_redis
from core.security import get_current_active_user, get_current_user
from core.rate_limit import rate_limit
from ..models.user import User
from schemas.preference import PreferenceCreate, PreferenceResponse, PreferenceUpdate
from ..services.preference import PreferenceService

router = APIRouter()
preference_service = PreferenceService()

@router.get("/", response_model=List[PreferenceResponse])
async def read_preferences(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve user's preferences.
    """
    preferences = preference_service.get_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return preferences

@router.post("/", response_model=PreferenceResponse)
async def create_preference(
    *,
    db: Session = Depends(get_db),
    preference_in: PreferenceCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new preference.
    """
    preference = preference_service.create_with_user(
        db=db,
        obj_in=preference_in,
        user_id=current_user.id
    )
    return preference

@router.put("/{user_id}", response_model=PreferenceResponse)
@rate_limit(times=100, period=3600)  # 100 requests per hour
async def update_preferences(
    user_id: int,
    preferences: PreferenceUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """
    تحديث تفضيلات المستخدم
    
    - **user_id**: معرف المستخدم
    - **preferences**: بيانات التفضيلات الجديدة
    """
    # التحقق من الصلاحيات
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="غير مصرح لك بتحديث هذه التفضيلات")
    
    service = PreferenceService(db)
    
    # التحقق من صحة التفضيلات
    if not await service.validate_preferences(preferences):
        raise HTTPException(status_code=400, detail="بيانات التفضيلات غير صالحة")
    
    # تحديث التفضيلات
    updated_preferences = await service.update_preferences(
        user_id=user_id,
        preferences=preferences
    )
    
    # حذف التفضيلات من الكاش
    cache_key = f"user_preferences:{user_id}"
    redis.delete(cache_key)
    
    # تحديث التوصيات في الخلفية
    background_tasks.add_task(
        service.update_recommendations,
        user_id=user_id
    )
    
    return updated_preferences

@router.get("/{user_id}", response_model=PreferenceResponse)
@rate_limit(times=200, period=3600)  # 200 requests per hour
async def get_preferences(
    user_id: int,
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis),
    current_user: User = Depends(get_current_user)
):
    """
    الحصول على تفضيلات المستخدم
    
    - **user_id**: معرف المستخدم
    """
    # التحقق من الصلاحيات
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="غير مصرح لك بالوصول إلى هذه التفضيلات")
    
    service = PreferenceService(db)
    
    # محاولة الحصول من الكاش
    cache_key = f"user_preferences:{user_id}"
    cached_preferences = redis.get(cache_key)
    
    if cached_preferences:
        return cached_preferences
    
    # الحصول من قاعدة البيانات
    preferences = await service.get_preferences(user_id)
    
    # تخزين في الكاش لمدة ساعة
    redis.setex(
        cache_key,
        timedelta(hours=1),
        preferences
    )
    
    return preferences

@router.delete("/{category}", response_model=PreferenceResponse)
async def delete_preference(
    *,
    db: Session = Depends(get_db),
    category: str,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete a preference.
    """
    preference = preference_service.get_by_category(
        db=db,
        user_id=current_user.id,
        category=category
    )
    if not preference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preference not found"
        )
    preference = preference_service.delete(db=db, id=preference.id)
    return preference

@router.get("/categories", response_model=List[str])
async def read_categories(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get user's preferred categories.
    """
    categories = preference_service.get_user_categories(
        db=db,
        user_id=current_user.id
    )
    return categories

@router.get("/tags", response_model=List[str])
async def read_tags(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get user's preferred tags.
    """
    tags = preference_service.get_user_tags(
        db=db,
        user_id=current_user.id
    )
    return tags 