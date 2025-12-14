"""
Tests for the sweets endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth import hash_password, create_access_token
from app.models import User, Sweet, UserRole


def test_search_sweets_empty(client: TestClient):
    """Test searching sweets when database is empty."""
    response = client.get("/sweets/search?q=chocolate")
    assert response.status_code == 200
    assert response.json() == []


def test_search_sweets_with_results(client: TestClient, db: Session):
    """Test searching sweets with matching results."""
    # Create test sweets
    sweet1 = Sweet(name="Chocolate Cake", description="Delicious chocolate", price=25.99)
    sweet2 = Sweet(name="Vanilla Cake", description="Plain vanilla", price=15.99)
    sweet3 = Sweet(name="Chocolate Donut", description="Chocolate donut", price=3.99)
    
    db.add_all([sweet1, sweet2, sweet3])
    db.commit()
    
    response = client.get("/sweets/search?q=chocolate")
    assert response.status_code == 200
    result = response.json()
    assert len(result) == 2
    names = {sweet["name"] for sweet in result}
    assert names == {"Chocolate Cake", "Chocolate Donut"}


def test_create_sweet_as_admin(client: TestClient, db: Session):
    """Test creating a sweet as an admin user."""
    # Create admin user
    admin = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    
    # Create token
    token = create_access_token({"sub": "admin"})
    
    # Create sweet
    sweet_data = {
        "name": "Croissant",
        "description": "French pastry",
        "price": 5.99
    }
    response = client.post(
        "/sweets",
        json=sweet_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "Croissant"
    assert result["description"] == "French pastry"
    assert result["price"] == 5.99


def test_create_sweet_as_user_forbidden(client: TestClient, db: Session):
    """Test that regular users cannot create sweets."""
    # Create regular user
    user = User(
        username="user",
        hashed_password=hash_password("user123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    
    # Create token
    token = create_access_token({"sub": "user"})
    
    # Try to create sweet
    sweet_data = {
        "name": "Croissant",
        "description": "French pastry",
        "price": 5.99
    }
    response = client.post(
        "/sweets",
        json=sweet_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403


def test_get_sweet_by_id(client: TestClient, db: Session):
    """Test getting a sweet by ID."""
    sweet = Sweet(name="Macaron", description="French cookie", price=2.99)
    db.add(sweet)
    db.commit()
    
    response = client.get(f"/sweets/{sweet.id}")
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Macaron"
    assert result["price"] == 2.99


def test_get_sweet_not_found(client: TestClient):
    """Test getting a non-existent sweet."""
    response = client.get("/sweets/999")
    assert response.status_code == 404


def test_update_sweet_as_admin(client: TestClient, db: Session):
    """Test updating a sweet as admin."""
    # Create sweet
    sweet = Sweet(name="Tart", description="Fruit tart", price=8.99)
    db.add(sweet)
    db.commit()
    sweet_id = sweet.id
    
    # Create admin user
    admin = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    
    # Create token
    token = create_access_token({"sub": "admin"})
    
    # Update sweet
    update_data = {
        "name": "Fruit Tart",
        "description": "Updated description",
        "price": 9.99
    }
    response = client.put(
        f"/sweets/{sweet_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Fruit Tart"
    assert result["price"] == 9.99


def test_delete_sweet_as_admin(client: TestClient, db: Session):
    """Test deleting a sweet as admin."""
    # Create sweet
    sweet = Sweet(name="Eclair", description="Chocolate eclair", price=4.99)
    db.add(sweet)
    db.commit()
    sweet_id = sweet.id
    
    # Create admin user
    admin = User(
        username="admin",
        hashed_password=hash_password("admin123"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    
    # Create token
    token = create_access_token({"sub": "admin"})
    
    # Delete sweet
    response = client.delete(
        f"/sweets/{sweet_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/sweets/{sweet_id}")
    assert get_response.status_code == 404


def test_delete_sweet_as_user_forbidden(client: TestClient, db: Session):
    """Test that regular users cannot delete sweets."""
    # Create sweet
    sweet = Sweet(name="Eclair", description="Chocolate eclair", price=4.99)
    db.add(sweet)
    db.commit()
    sweet_id = sweet.id
    
    # Create regular user
    user = User(
        username="user",
        hashed_password=hash_password("user123"),
        role=UserRole.USER
    )
    db.add(user)
    db.commit()
    
    # Create token
    token = create_access_token({"sub": "user"})
    
    # Try to delete sweet
    response = client.delete(
        f"/sweets/{sweet_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
