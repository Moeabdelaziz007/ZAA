"""
Database configuration and session management.
This module handles database connections and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from .config import DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

@contextmanager
def get_db():
    """
    Context manager for database sessions.
    Ensures proper session cleanup after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    """
    Base.metadata.create_all(bind=engine)

def get_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="المستخدم غير موجود")
        return user
    except SQLAlchemyError as e:
        logger.error(f"خطأ في قاعدة البيانات: {str(e)}")
        raise HTTPException(status_code=500, detail="حدث خطأ في الخادم")