"""
Item endpoints.
This module contains the item-related API endpoints.
"""

from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import get_current_active_user
from models.user import User
from schemas.item import ItemCreate, ItemResponse, ItemUpdate
from services.item import ItemService

router = APIRouter()
item_service = ItemService()

@router.get("/", response_model=List[ItemResponse])
async def read_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Retrieve items.
    """
    items = item_service.get_all(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=ItemResponse)
async def create_item(
    *,
    db: Session = Depends(get_db),
    item_in: ItemCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create new item.
    """
    item = item_service.create_with_owner(
        db=db,
        obj_in=item_in,
        owner_id=current_user.id
    )
    return item

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get item by ID.
    """
    item = item_service.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    item_in: ItemUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update an item.
    """
    item = item_service.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    item = item_service.update(db, db_obj=item, obj_in=item_in)
    return item

@router.delete("/{item_id}", response_model=ItemResponse)
async def delete_item(
    *,
    db: Session = Depends(get_db),
    item_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete an item.
    """
    item = item_service.get(db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    if item.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    item = item_service.delete(db, id=item_id)
    return item 