"""
Interaction endpoints.
This module contains the interaction-related API endpoints.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_active_user
from models.user import User
from schemas.interaction import InteractionCreate, InteractionResponse
from services.interaction import InteractionService

router = APIRouter()
interaction_service = InteractionService()

@router.post("/", response_model=InteractionResponse)
async def create_interaction(
    *,
    db: Session = Depends(get_db),
    interaction_in: InteractionCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new interaction.
    """
    interaction = interaction_service.create_with_user(
        db=db,
        obj_in=interaction_in,
        user_id=current_user.id
    )
    return interaction

@router.get("/", response_model=List[InteractionResponse])
async def read_interactions(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve user's interactions.
    """
    interactions = interaction_service.get_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return interactions

@router.get("/{interaction_id}", response_model=InteractionResponse)
async def read_interaction(
    *,
    db: Session = Depends(get_db),
    interaction_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get interaction by ID.
    """
    interaction = interaction_service.get(db, id=interaction_id)
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    if interaction.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return interaction

@router.delete("/{interaction_id}", response_model=InteractionResponse)
async def delete_interaction(
    *,
    db: Session = Depends(get_db),
    interaction_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete an interaction.
    """
    interaction = interaction_service.get(db, id=interaction_id)
    if not interaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found"
        )
    if interaction.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    interaction = interaction_service.delete(db, id=interaction_id)
    return interaction 