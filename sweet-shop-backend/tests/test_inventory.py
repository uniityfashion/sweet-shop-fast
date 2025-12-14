"""
Tests for the inventory endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth import hash_password, create_access_token
from app.models import User, Sweet, UserRole


def test_get_inventory_empty(client: TestClient):
    """Test getting inventory when no sweets exist."""
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json() == []


def test_get_inventory_with_sweets(client: TestClient, db: Session):
    """Test getting inventory with sweets."""
    # Create test sweets
    sweet1 = Sweet(name="Candy", description="Sweet candy", price=1.99, stock=100)
    sweet2 = Sweet(name="Chocolate", description="Dark chocolate", price=5.99, stock=50)
    
    db.add_all([sweet1, sweet2])
    db.commit()
    
    response = client.get("/inventory")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    assert result[0]["name"] == "Candy"
    assert result[0]["stock"] == 100


def test_restock_sweet_as_admin(client: TestClient, db: Session):
    """Test restocking a sweet as admin."""
    # Create sweet
    sweet = Sweet(name="Donut", description="Glazed donut", price=2.99, stock=10)
    db.add(sweet)
    db.commit()
    sweet_id = sweet.id
    
    # Create admin
    admin = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    
    token = create_access_token({"sub": "admin"})
    
    # Restock
    response = client.post(
        f"/inventory/{sweet_id}/restock",
        json={"quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["new_stock"] == 60
    assert "restocked" in result["message"].lower()


def test_restock_sweet_as_user_forbidden(client: TestClient, db: Session):
    """Test that regular users cannot restock."""
    # Create sweet
    sweet = Sweet(name="Donut", description="Glazed donut", price=2.99, stock=10)
    db.add(sweet)
    db.commit()
    sweet_id = sweet.id
    
    # Create user
    user = User(
        username="user",
        hashed_password=hash_password("user123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    
    token = create_access_token({"sub": "user"})
    
    # Try to restock
    response = client.post(
        f"/inventory/{sweet_id}/restock",
        json={"quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403


def test_purchase_sweet_reduces_stock(client: TestClient, db: Session):
    """Test purchasing a sweet reduces stock."""
    # Create sweet
    sweet = Sweet(name="Cookie", description="Chocolate chip", price=1.99, stock=20)
    db.add(sweet)
    db.commit()
    sweet_id = sweet.id
    
    # Create user
    user = User(
        username="user",
        hashed_password=hash_password("user123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    
    token = create_access_token({"sub": "user"})
    
    # Purchase
    response = client.post(
        f"/inventory/{sweet_id}/purchase",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["new_stock"] == 15
    assert "purchased" in result["message"].lower()


def test_purchase_sweet_insufficient_stock(client: TestClient, db: Session):
    """Test purchasing when insufficient stock."""
    # Create sweet with low stock
    sweet = Sweet(name="Cookie", description="Chocolate chip", price=1.99, stock=3)
    db.add(sweet)
    db.commit()
    sweet_id = sweet.id
    
    # Create user
    user = User(
        username="user",
        hashed_password=hash_password("user123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    
    token = create_access_token({"sub": "user"})
    
    # Try to purchase more than available
    response = client.post(
        f"/inventory/{sweet_id}/purchase",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400


def test_purchase_sweet_not_found(client: TestClient, db: Session):
    """Test purchasing non-existent sweet."""
    # Create user
    user = User(
        username="user",
        hashed_password=hash_password("user123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    
    token = create_access_token({"sub": "user"})
    
    # Try to purchase
    response = client.post(
        f"/inventory/999/purchase",
        json={"quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
