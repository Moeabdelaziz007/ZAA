from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..core.auth import get_current_user, authenticate_user
from ..models.user import User
from ..services.emotion import EmotionService
from ..services.chat import ChatService
from ..services.skills import SkillsService
from ..services.dashboard import DashboardService
from ..services.settings import SettingsService

router = APIRouter()

# Auth Routes
@router.post("/auth/login")
async def login(username: str, password: str):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("/auth/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {"user": current_user}

# Dashboard Routes
@router.get("/dashboard/stats")
async def get_stats(current_user: User = Depends(get_current_user)):
    dashboard_service = DashboardService()
    return await dashboard_service.get_stats(current_user.id)

@router.get("/dashboard/interactions")
async def get_interactions(current_user: User = Depends(get_current_user)):
    dashboard_service = DashboardService()
    return await dashboard_service.get_interactions(current_user.id)

@router.get("/dashboard/activities")
async def get_activities(current_user: User = Depends(get_current_user)):
    dashboard_service = DashboardService()
    return await dashboard_service.get_activities(current_user.id)

# Emotion Routes
@router.get("/emotions/weekly")
async def get_weekly_emotions(current_user: User = Depends(get_current_user)):
    emotion_service = EmotionService()
    return await emotion_service.get_weekly_analysis(current_user.id)

@router.post("/emotions/analyze")
async def analyze_emotion(text: str, current_user: User = Depends(get_current_user)):
    emotion_service = EmotionService()
    return await emotion_service.analyze_text(text)

# Chat Routes
@router.post("/chat/message")
async def send_message(message: str, current_user: User = Depends(get_current_user)):
    chat_service = ChatService()
    return await chat_service.process_message(message, current_user.id)

# Skills Routes
@router.get("/skills")
async def get_skills(current_user: User = Depends(get_current_user)):
    skills_service = SkillsService()
    return await skills_service.get_user_skills(current_user.id)

@router.post("/skills/create-sibling")
async def create_sibling(data: dict, current_user: User = Depends(get_current_user)):
    skills_service = SkillsService()
    return await skills_service.create_sibling(data, current_user.id)

# Settings Routes
@router.get("/settings")
async def get_settings(current_user: User = Depends(get_current_user)):
    settings_service = SettingsService()
    return await settings_service.get_user_settings(current_user.id)

@router.post("/settings")
async def update_settings(settings: dict, current_user: User = Depends(get_current_user)):
    settings_service = SettingsService()
    return await settings_service.update_user_settings(current_user.id, settings) 