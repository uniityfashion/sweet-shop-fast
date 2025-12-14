"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from app.models import UserRole


# User Schemas
class UserBase(BaseModel):
    """Base schema for user data."""
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(UserBase):
    """Schema for user login."""
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    role: UserRole

    class Config:
        from_attributes = True


# Token Schemas
class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None


# Sweet Schemas
class SweetBase(BaseModel):
    """Base schema for sweet data."""
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)


class SweetCreate(SweetBase):
    """Schema for creating a sweet."""
    pass


class SweetUpdate(BaseModel):
    """Schema for updating a sweet."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)


class SweetResponse(SweetBase):
    """Schema for sweet response."""
    id: int

    class Config:
        from_attributes = True


# Inventory Schemas
class PurchaseRequest(BaseModel):
    """Schema for purchase request."""
    quantity: int = Field(default=1, ge=1)


class RestockRequest(BaseModel):
    """Schema for restock request."""
    quantity: int = Field(..., ge=1)


class InventoryResponse(BaseModel):
    """Schema for inventory response."""
    sweet_id: int
    new_quantity: int
    message: str
