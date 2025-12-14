"""
Authentication and authorization logic using JWT and OAuth2.
"""
from datetime import datetime, timedelta
from typing import Optional
import hashlib
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.models import User, UserRole
from app.schemas import TokenData
from app.database import get_db

# Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # Should be in environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    """
    Hash a password using SHA256.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
    """
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data for the token
        expires_delta: Token expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current user from JWT token.
    
    Args:
        token: JWT token from request
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current admin user. Raises exception if user is not admin.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if user is admin
        
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def authenticate_user(
    db: Session,
    username: str,
    password: str
) -> Optional[User]:
    """
    Authenticate user by username and password.
    
    Args:
        db: Database session
        username: Username
        password: Plain text password
        
    Returns:
        User object if authentication successful, None otherwise
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
