"""
User schemas.
This module contains Pydantic models for user-related operations.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    """Base user schema."""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """User creation schema."""
    email: EmailStr
    password: constr(min_length=8)
    full_name: str

class UserUpdate(UserBase):
    """User update schema."""
    password: Optional[constr(min_length=8)] = None

class UserInDBBase(UserBase):
    """Base user in database schema."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(UserInDBBase):
    """User response schema."""
    pass

class UserInDB(UserInDBBase):
    """User in database schema."""
    hashed_password: str 