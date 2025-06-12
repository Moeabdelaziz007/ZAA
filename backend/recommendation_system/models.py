from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # User preferences and behavior data
    preferences = Column(JSON, default={})
    behavior_data = Column(JSON, default={})
    
    # Relationships
    interactions = relationship("UserInteraction", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    category = Column(String, index=True)
    features = Column(JSON)  # Item features for content-based filtering
    metadata = Column(JSON)  # Additional item metadata
    
    # Relationships
    interactions = relationship("UserInteraction", back_populates="item")
    recommendations = relationship("Recommendation", back_populates="item")

class UserInteraction(Base):
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    interaction_type = Column(String)  # view, like, share, purchase, etc.
    interaction_value = Column(Float)  # Rating or weight of interaction
    timestamp = Column(DateTime, default=datetime.utcnow)
    context = Column(JSON)  # Additional context about the interaction
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    item = relationship("Item", back_populates="interactions")

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    score = Column(Float)  # Recommendation score
    algorithm = Column(String)  # Algorithm used for recommendation
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # Additional recommendation metadata
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    item = relationship("Item", back_populates="recommendations") 