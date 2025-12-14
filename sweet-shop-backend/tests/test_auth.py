"""
Test suite for authentication endpoints.
These tests are initially failing and will be fixed in Step 3b.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User, UserRole
from app.auth import hash_password


def test_register_user_success(client: TestClient, db: Session):
    """Test successful user registration."""
    response = client.post(
        "/auth/register",
        json={"username": "newuser", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["id"] is not None
    assert data["role"] == "user"


def test_register_user_duplicate_username(client: TestClient, db: Session):
    """Test registration with duplicate username."""
    # Create first user
    user = User(
        username="testuser",
        hashed_password=hash_password("password123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()

    # Try to create user with same username
    response = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "password456"}
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_user_invalid_password(client: TestClient):
    """Test registration with too short password."""
    response = client.post(
        "/auth/register",
        json={"username": "newuser", "password": "short"}
    )
    assert response.status_code == 422  # Validation error


def test_login_user_success(client: TestClient, db: Session):
    """Test successful user login."""
    # Create user
    user = User(
        username="testuser",
        hashed_password=hash_password("password123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()

    # Login
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_user_invalid_credentials(client: TestClient, db: Session):
    """Test login with invalid credentials."""
    # Create user
    user = User(
        username="testuser",
        hashed_password=hash_password("password123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()

    # Try to login with wrong password
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_login_user_not_found(client: TestClient):
    """Test login with non-existent user."""
    response = client.post(
        "/auth/login",
        json={"username": "nonexistent", "password": "password123"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


def test_get_current_user_with_valid_token(client: TestClient, db: Session):
    """Test getting current user with valid token."""
    # Create user
    user = User(
        username="testuser",
        hashed_password=hash_password("password123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()

    # Login to get token
    login_response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "user"


def test_get_current_user_without_token(client: TestClient):
    """Test getting current user without token."""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_get_current_user_with_invalid_token(client: TestClient):
    """Test getting current user with invalid token."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
