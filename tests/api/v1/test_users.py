from __future__ import annotations

from types import SimpleNamespace

from app.api.deps import get_admin_user, get_current_user
from app.models.user import UserRole


def test_get_users_requires_admin(client):
    response = client.get("/users/")

    assert response.status_code == 401


def test_get_users_returns_list_for_admin(client, admin_user):
    app = client.app
    app.dependency_overrides[get_admin_user] = lambda: admin_user

    response = client.get("/users/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_create_user_requires_admin(client):
    payload = {
        "name": "Tester",
        "email": "tester@example.com",
        "login": "tester-login",
        "password": "123456",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 401


def test_create_user_creates_record_for_admin(client, admin_user):
    app = client.app
    app.dependency_overrides[get_admin_user] = lambda: admin_user
    payload = {
        "name": "Tester",
        "email": "tester@example.com",
        "login": "tester-login",
        "phone_number": "+380671112233",
        "password": "123456",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]
    assert response.json()["email"] == payload["email"]
    assert response.json()["login"] == payload["login"]
    assert "password" not in response.json()


def test_update_user_updates_existing_record(client, created_user):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: created_user
    payload = {
        "name": "Updated Name",
        "email": "updated@example.com",
        "login": "updated-login",
        "phone_number": "+380991112233",
    }

    response = client.put(f"/users/{created_user.id}", json=payload)

    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["email"] == payload["email"]
    assert response.json()["login"] == payload["login"]


def test_update_user_returns_404_for_missing_user(client):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=999, role=UserRole.ADMIN)
    response = client.put(
        "/users/999",
        json={"name": "Nobody", "email": "nobody@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_returns_403_for_other_non_admin_user(client, created_user):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=created_user.id + 1,
        role=UserRole.USER,
    )

    response = client.put(
        f"/users/{created_user.id}",
        json={"name": "Blocked update"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_delete_user_deletes_own_account(client, created_user):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=created_user.id,
        role=UserRole.USER,
    )

    response = client.delete(f"/users/{created_user.id}")

    assert response.status_code == 200
    assert response.json() == {"message": "deleted"}


def test_delete_user_returns_403_for_other_user(client, created_user):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=created_user.id + 1,
        role=UserRole.USER,
    )

    response = client.delete(f"/users/{created_user.id}")

    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


def test_delete_user_returns_404_for_missing_user(client):
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(id=999, role=UserRole.ADMIN)

    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_role_promotes_user_by_login(client, admin_user, created_user):
    app = client.app
    app.dependency_overrides[get_admin_user] = lambda: admin_user

    response = client.patch(
        f"/users/by-login/{created_user.login}/role",
        json={"role": "staff"},
    )

    assert response.status_code == 200
    assert response.json()["role"] == "staff"
