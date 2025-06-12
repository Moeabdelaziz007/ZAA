"""
User model.
This module contains the SQLAlchemy model for users.
"""

from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from typing import Optional
from ..utils.database import get_db

from core.database import Base

class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = relationship("Item", back_populates="owner")
    interactions = relationship("Interaction", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

    @classmethod
    async def get_by_username(cls, username: str) -> Optional["User"]:
        async with get_db() as db:
            return await db.query(cls).filter(cls.username == username).first()

    @classmethod
    async def get_by_email(cls, email: str) -> Optional["User"]:
        async with get_db() as db:
            return await db.query(cls).filter(cls.email == email).first()

    @classmethod
    async def create(cls, username: str, email: str, password: str, full_name: str) -> "User":
        from ..core.auth import get_password_hash
        user = cls(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            full_name=full_name
        )
        async with get_db() as db:
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        } 