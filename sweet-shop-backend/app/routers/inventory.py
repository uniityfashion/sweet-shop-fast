"""
Inventory management endpoints for tracking stock and purchases.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Sweet, User, UserRole
from app.schemas import SweetResponse
from app.auth import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])


class InventoryResponse(SweetResponse):
    """Extended response that includes stock information."""
    pass


class RestockRequest:
    """Request model for restocking."""
    def __init__(self, quantity: int):
        self.quantity = quantity


class PurchaseRequest:
    """Request model for purchases."""
    def __init__(self, quantity: int):
        self.quantity = quantity


@router.get("", response_model=List[SweetResponse])
def get_inventory(db: Session = Depends(get_db)):
    """
    Get complete inventory of all sweets.
    
    Args:
        db: Database session
        
    Returns:
        List of all sweets with stock information
    """
    sweets = db.query(Sweet).all()
    return sweets


@router.post("/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    quantity_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Restock a sweet (admin only).
    
    Args:
        sweet_id: Sweet ID to restock
        quantity_data: Dictionary with 'quantity' key
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated inventory information
        
    Raises:
        403: If user is not an admin
        404: If sweet not found
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can restock items"
        )
    
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    quantity = quantity_data.get("quantity", 0)
    sweet.stock += quantity
    db.commit()
    db.refresh(sweet)
    
    return {
        "sweet_id": sweet_id,
        "new_stock": sweet.stock,
        "message": f"Successfully restocked {quantity} units"
    }


@router.post("/{sweet_id}/purchase")
def purchase_sweet(
    sweet_id: int,
    quantity_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Purchase a sweet (reduces stock).
    
    Args:
        sweet_id: Sweet ID to purchase
        quantity_data: Dictionary with 'quantity' key
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        Updated inventory information
        
    Raises:
        400: If insufficient stock
        404: If sweet not found
    """
    sweet = db.query(Sweet).filter(Sweet.id == sweet_id).first()
    
    if not sweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )
    
    quantity = quantity_data.get("quantity", 0)
    
    if sweet.stock < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Available: {sweet.stock}, Requested: {quantity}"
        )
    
    sweet.stock -= quantity
    db.commit()
    db.refresh(sweet)
    
    return {
        "sweet_id": sweet_id,
        "new_stock": sweet.stock,
        "message": f"Successfully purchased {quantity} units"
    }
