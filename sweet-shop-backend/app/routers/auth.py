"""
Authentication router for user registration and login.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserRole
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.auth import (
    hash_password,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Created user information
        
    Raises:
        HTTPException: If username already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        User.username == user_data.username
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        role=UserRole.USER
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
) -> Token:
    """
    Login user and return JWT access token.
    
    Args:
        credentials: User login credentials
        db: Database session
        
    Returns:
        Access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(db, credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user information
    """
    return current_user
