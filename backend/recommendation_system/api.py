from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta

from database import get_db
from .models import User, Item, UserInteraction, Recommendation
from .recommender import HybridRecommender
from .schemas import (
    UserInteractionCreate,
    RecommendationResponse,
    UserPreferencesUpdate
)

router = APIRouter()
recommender = HybridRecommender()

@router.post("/interactions/", response_model=Dict)
async def create_interaction(
    interaction: UserInteractionCreate,
    db: Session = Depends(get_db)
):
    """تسجيل تفاعل جديد للمستخدم"""
    # إنشاء تفاعل جديد
    db_interaction = UserInteraction(
        user_id=interaction.user_id,
        item_id=interaction.item_id,
        interaction_type=interaction.interaction_type,
        interaction_value=interaction.interaction_value,
        context=interaction.context
    )
    db.add(db_interaction)
    db.commit()
    
    # تحديث التوصيات
    recommender.update_recommendations(interaction.dict())
    
    return {"status": "success", "message": "Interaction recorded"}

@router.get("/recommendations/{user_id}", response_model=List[RecommendationResponse])
async def get_recommendations(
    user_id: int,
    n_recommendations: int = 10,
    db: Session = Depends(get_db)
):
    """الحصول على توصيات للمستخدم"""
    # التحقق من وجود المستخدم
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # الحصول على التوصيات
    recommendations = recommender.get_recommendations(user_id, n_recommendations)
    
    # حفظ التوصيات في قاعدة البيانات
    for rec in recommendations:
        db_recommendation = Recommendation(
            user_id=user_id,
            item_id=rec['item_id'],
            score=rec['score'],
            algorithm=rec['algorithm'],
            metadata={"timestamp": datetime.utcnow().isoformat()}
        )
        db.add(db_recommendation)
    
    db.commit()
    
    return recommendations

@router.put("/users/{user_id}/preferences", response_model=Dict)
async def update_user_preferences(
    user_id: int,
    preferences: UserPreferencesUpdate,
    db: Session = Depends(get_db)
):
    """تحديث تفضيلات المستخدم"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # تحديث التفضيلات
    current_preferences = user.preferences or {}
    current_preferences.update(preferences.dict())
    user.preferences = current_preferences
    
    db.commit()
    
    return {"status": "success", "message": "Preferences updated"}

@router.get("/items/{item_id}/similar", response_model=List[Dict])
async def get_similar_items(
    item_id: int,
    n_items: int = 5,
    db: Session = Depends(get_db)
):
    """الحصول على عناصر مشابهة"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # الحصول على العناصر المشابهة باستخدام نموذج المحتوى
    item_features = recommender.content_model.transform([str(item.features)])
    similarities = recommender.get_content_based_scores([item.features])
    
    # ترتيب العناصر حسب التشابه
    similar_items = []
    top_indices = np.argsort(-similarities)[1:n_items+1]  # استبعاد العنصر نفسه
    
    for idx in top_indices:
        similar_item = db.query(Item).filter(Item.id == int(idx)).first()
        if similar_item:
            similar_items.append({
                "item_id": similar_item.id,
                "title": similar_item.title,
                "similarity_score": float(similarities[idx])
            })
    
    return similar_items

@router.get("/users/{user_id}/behavior", response_model=Dict)
async def get_user_behavior(
    user_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """تحليل سلوك المستخدم"""
    # الحصول على تفاعلات المستخدم في الفترة المحددة
    start_date = datetime.utcnow() - timedelta(days=days)
    interactions = db.query(UserInteraction).filter(
        UserInteraction.user_id == user_id,
        UserInteraction.timestamp >= start_date
    ).all()
    
    # تحليل السلوك
    behavior_analysis = {
        "total_interactions": len(interactions),
        "interaction_types": {},
        "categories": {},
        "time_distribution": {
            "morning": 0,
            "afternoon": 0,
            "evening": 0,
            "night": 0
        }
    }
    
    for interaction in interactions:
        # تحليل أنواع التفاعل
        behavior_analysis["interaction_types"][interaction.interaction_type] = \
            behavior_analysis["interaction_types"].get(interaction.interaction_type, 0) + 1
        
        # تحليل الفئات
        item = db.query(Item).filter(Item.id == interaction.item_id).first()
        if item:
            behavior_analysis["categories"][item.category] = \
                behavior_analysis["categories"].get(item.category, 0) + 1
        
        # تحليل التوقيت
        hour = interaction.timestamp.hour
        if 6 <= hour < 12:
            behavior_analysis["time_distribution"]["morning"] += 1
        elif 12 <= hour < 17:
            behavior_analysis["time_distribution"]["afternoon"] += 1
        elif 17 <= hour < 22:
            behavior_analysis["time_distribution"]["evening"] += 1
        else:
            behavior_analysis["time_distribution"]["night"] += 1
    
    return behavior_analysis 