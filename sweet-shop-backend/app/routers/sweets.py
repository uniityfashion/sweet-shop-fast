"""
Sweets endpoints for managing sweet shop items.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Sweet, User, UserRole
from app.schemas import SweetCreate, SweetResponse
from app.auth import get_current_user

router = APIRouter(prefix="/sweets", tags=["sweets"])


@router.get("/search", response_model=List[SweetResponse])
def search_sweets(q: str = "", db: Session = Depends(get_db)):
    """
    Search for sweets by name or description.
    
    Args:
        q: Search query string
        db: Database session
        
    Returns:
        List of sweets matching the query
    """
    query = db.query(Sweet)
    
    if q:
        query = query.filter(
            (Sweet.name.ilike(f"%{q}%")) | (Sweet.description.ilike(f"%{q}%"))
        )
    
    sweets = query.all()
    return sweets


@router.post("", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
def create_sweet(
    sweet: SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new sweet (admin only).
    
    Args:
        sweet: Sweet data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Created sweet
        
    Raises:
        403: If user is not an admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create sweets"
        )
    
    sweet_data = sweet.model_dump()
    sweet_data['stock'] = sweet_data.get('stock', 0)
    db_sweet = Sweet(**sweet_data)
    db.add(db_sweet)
    db.commit()
    db.refresh(db_sweet)
    
    return db_sweet


@router.get("/{sweet_id}", response_model=SweetResponse)
def get_sweet(sweet_id: int, db: Session = Depends(get_db)):
    """
    Get a sweet by ID.
    
    Args:
        sweet_id: Sweet ID
        db: Database session
        
    Returns:
        Sweet details
        
    Raises:
        404: If sweet not found
    """
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    return sweet


@router.put("/{sweet_id}", response_model=SweetResponse)
def update_sweet(
    sweet_id: int,
    sweet: SweetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a sweet (admin only).
    
    Args:
        sweet_id: Sweet ID
        sweet: Updated sweet data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated sweet
        
    Raises:
        403: If user is not an admin
        404: If sweet not found
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update sweets"
        )
    
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    for field, value in sweet.model_dump(exclude_unset=True).items():
        setattr(db_sweet, field, value)
    
    db.commit()
    db.refresh(db_sweet)
    
    return db_sweet


@router.delete("/{sweet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sweet(
    sweet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a sweet (admin only).
    
    Args:
        sweet_id: Sweet ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        403: If user is not an admin
        404: If sweet not found
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete sweets"
        )
    
    db_sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not db_sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    db.delete(db_sweet)
    db.commit()
