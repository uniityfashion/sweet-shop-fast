"""
Pytest configuration and fixtures.
"""
# SET ENVIRONMENT VARIABLE FIRST, before any imports
import os
os.environ["TESTING"] = "true"

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

# NOW import app modules
from app.database import Base, get_db, SessionLocal
from app.main import app

# Create in-memory test database engine with StaticPool
from sqlalchemy.pool import StaticPool

TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)

# Reconfigure SessionLocal to use TEST_ENGINE
SessionLocal.configure(bind=TEST_ENGINE, expire_on_commit=False)


@pytest.fixture(scope="function")
def db() -> Session:
    """
    Fixture that provides a test database session.
    Creates tables before each test, drops them after.
    """
    # Create all tables in TEST_ENGINE
    Base.metadata.create_all(bind=TEST_ENGINE)
    
    # Create session using the reconfigured SessionLocal
    db_session = SessionLocal()
    
    yield db_session
    
    db_session.close()
    # Drop all tables after test
    Base.metadata.drop_all(bind=TEST_ENGINE)


@pytest.fixture(scope="function")
def client(db: Session):
    """
    Fixture that provides a test client with overridden get_db.
    Uses the same session that was created in the db fixture.
    """
    # Verify tables exist BEFORE creating override
    inspector = inspect(TEST_ENGINE)
    tables = inspector.get_table_names()
    print(f"\nDEBUG [client fixture START]: Tables in TEST_ENGINE: {tables}")
    
    def override_get_db():
        print(f"DEBUG [override_get_db CALLED]: About to yield session")
        try:
            # Double check tables still exist
            inspector = inspect(db.get_bind())
            tables = inspector.get_table_names()
            print(f"DEBUG [override_get_db]: Tables visible: {tables}")
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    print(f"DEBUG [client fixture]: Dependency override set")
    yield TestClient(app)
    print(f"DEBUG [client fixture END]: Cleaning up")
    app.dependency_overrides.clear()
