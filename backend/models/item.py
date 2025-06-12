"""
Item model.
This module contains the SQLAlchemy model for items.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import relationship

from core.database import Base

class Item(Base):
    """Item model."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    category = Column(String, index=True)
    tags = Column(ARRAY(String), default=[])
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="items")
    interactions = relationship("Interaction", back_populates="item")

    def __repr__(self):
        return f"<Item {self.title}>" 