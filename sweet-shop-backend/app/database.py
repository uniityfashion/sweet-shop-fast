"""
Database configuration and session management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

# SQLite database URL - use test database if running tests
if os.getenv("TESTING"):
    DATABASE_URL = "sqlite:///:memory:"
    # Use StaticPool to ensure all connections share the same in-memory database
    engine = create_engine(
        DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
else:
    DATABASE_URL = "sqlite:///./sweet_shop.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session.
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
