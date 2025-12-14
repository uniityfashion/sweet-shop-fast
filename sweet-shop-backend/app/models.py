"""
SQLAlchemy ORM models for the Sweet Shop Management System.
"""
from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"


class User(Base):
    """
    User model representing system users.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"


class Sweet(Base):
    """
    Sweet model representing products in the shop.
    """
    __tablename__ = "sweets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return (
            f"<Sweet(id={self.id}, name={self.name}, description={self.description}, "
            f"price={self.price}, stock={self.stock})>"
        )
