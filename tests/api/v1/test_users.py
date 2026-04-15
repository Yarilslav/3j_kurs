from __future__ import annotations

from types import SimpleNamespace

from app.api.deps import get_current_user


def test_get_users_returns_empty_list(client):
    response = client.get("/users/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_user_creates_record(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secret123",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]
    assert response.json()["email"] == payload["email"]
    assert "password" not in response.json()


def test_update_user_updates_existing_record(client, created_user):
    payload = {
        "name": "Updated Name",
        "email": "updated@example.com",
    }

    response = client.put(f"/users/{created_user.id}", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["email"] == payload["email"]


def test_update_user_returns_404_for_missing_user(client):
    response = client.put(
        "/users/999",
        json={"name": "Nobody", "email": "nobody@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_delete_user_deletes_own_account(client, created_user):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=created_user.id)

    response = client.delete(f"/users/{created_user.id}")

    assert response.status_code == 200
    assert response.json() == {"message": "deleted"}


def test_delete_user_returns_403_for_other_user(client, created_user):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=created_user.id + 1)

    response = client.delete(f"/users/{created_user.id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_delete_user_returns_404_for_missing_user(client):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=999)

    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
