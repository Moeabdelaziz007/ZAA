"""
Authentication schemas.
This module contains Pydantic models for authentication.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    """Token schema."""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: Optional[int] = None

class EmailVerification(BaseModel):
    """Email verification schema."""
    email: EmailStr

class PasswordReset(BaseModel):
    """Password reset schema."""
    email: EmailStr

class PasswordChange(BaseModel):
    """Password change schema."""
    current_password: str
    new_password: str 