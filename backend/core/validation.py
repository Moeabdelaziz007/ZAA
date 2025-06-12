"""
نظام التحقق من البيانات
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator, EmailStr
from enum import Enum

class InteractionType(str, Enum):
    """أنواع التفاعلات"""
    VIEW = "view"
    LIKE = "like"
    PURCHASE = "purchase"
    SHARE = "share"

class UserBase(BaseModel):
    """نموذج المستخدم الأساسي"""
    email: EmailStr = Field(..., description="البريد الإلكتروني")
    full_name: str = Field(..., min_length=2, max_length=100, description="الاسم الكامل")
    is_active: bool = Field(True, description="حالة الحساب")
    is_admin: bool = Field(False, description="صلاحيات المدير")

class UserCreate(UserBase):
    """نموذج إنشاء مستخدم"""
    password: str = Field(..., min_length=8, description="كلمة المرور")
    
    @validator('password')
    def password_strength(cls, v):
        """التحقق من قوة كلمة المرور"""
        if not any(c.isupper() for c in v):
            raise ValueError("يجب أن تحتوي كلمة المرور على حرف كبير")
        if not any(c.islower() for c in v):
            raise ValueError("يجب أن تحتوي كلمة المرور على حرف صغير")
        if not any(c.isdigit() for c in v):
            raise ValueError("يجب أن تحتوي كلمة المرور على رقم")
        return v

class UserUpdate(BaseModel):
    """نموذج تحديث المستخدم"""
    email: Optional[EmailStr] = Field(None, description="البريد الإلكتروني")
    full_name: Optional[str] = Field(None, min_length=2, max_length=100, description="الاسم الكامل")
    password: Optional[str] = Field(None, min_length=8, description="كلمة المرور")
    is_active: Optional[bool] = Field(None, description="حالة الحساب")

class ItemBase(BaseModel):
    """نموذج العنصر الأساسي"""
    title: str = Field(..., min_length=3, max_length=200, description="عنوان العنصر")
    description: str = Field(..., min_length=10, description="وصف العنصر")
    category: str = Field(..., description="الفئة")
    image_url: str = Field(..., description="رابط الصورة")
    price: float = Field(..., gt=0, description="السعر")
    rating: float = Field(..., ge=1, le=5, description="التقييم")

class ItemCreate(ItemBase):
    """نموذج إنشاء عنصر"""
    pass

class ItemUpdate(BaseModel):
    """نموذج تحديث عنصر"""
    title: Optional[str] = Field(None, min_length=3, max_length=200, description="عنوان العنصر")
    description: Optional[str] = Field(None, min_length=10, description="وصف العنصر")
    category: Optional[str] = Field(None, description="الفئة")
    image_url: Optional[str] = Field(None, description="رابط الصورة")
    price: Optional[float] = Field(None, gt=0, description="السعر")
    rating: Optional[float] = Field(None, ge=1, le=5, description="التقييم")

class InteractionCreate(BaseModel):
    """نموذج إنشاء تفاعل"""
    item_id: int = Field(..., description="معرف العنصر")
    interaction_type: InteractionType = Field(..., description="نوع التفاعل")
    
    @validator('interaction_type')
    def validate_interaction_type(cls, v):
        """التحقق من نوع التفاعل"""
        if v not in InteractionType:
            raise ValueError("نوع تفاعل غير صالح")
        return v

class PreferenceCreate(BaseModel):
    """نموذج إنشاء تفضيل"""
    category: str = Field(..., description="الفئة")
    weight: float = Field(..., ge=0, le=1, description="الوزن")
    
    @validator('weight')
    def validate_weight(cls, v):
        """التحقق من الوزن"""
        if not 0 <= v <= 1:
            raise ValueError("يجب أن يكون الوزن بين 0 و 1")
        return v

class RecommendationRequest(BaseModel):
    """نموذج طلب التوصيات"""
    limit: int = Field(10, ge=1, le=50, description="عدد التوصيات")
    categories: Optional[List[str]] = Field(None, description="الفئات المفضلة")
    
    @validator('limit')
    def validate_limit(cls, v):
        """التحقق من الحد الأقصى"""
        if v > 50:
            raise ValueError("لا يمكن طلب أكثر من 50 توصية")
        return v

class ErrorResponse(BaseModel):
    """نموذج استجابة الخطأ"""
    detail: str = Field(..., description="رسالة الخطأ")
    code: str = Field(..., description="رمز الخطأ")
    timestamp: datetime = Field(default_factory=datetime.now, description="وقت الخطأ")
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "بيانات غير صالحة",
                "code": "VALIDATION_ERROR",
                "timestamp": "2024-03-20T12:00:00"
            }
        } 