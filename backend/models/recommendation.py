"""
Recommendation model.
This module contains the SQLAlchemy model for recommendations.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from core.database import Base

class Recommendation(Base):
    """Recommendation model."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    score = Column(Float, nullable=False)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="recommendations")
    item = relationship("Item", back_populates="recommendations")

    def __repr__(self):
        return f"<Recommendation {self.id}>" 