from __future__ import annotations


def test_register_creates_user(client):
    response = client.post(
        "/register",
        json={
            "name": "Bob",
            "email": "bob@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "bob@example.com"


def test_register_rejects_duplicate_email(client, created_user):
    response = client.post(
        "/register",
        json={
            "name": "Another User",
            "email": created_user.email,
            "password": "secret123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_with_email_returns_token_and_cookie(client, created_user):
    response = client.post(
        "/login",
        json={"login": created_user.email, "password": "secret123"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
    assert "access_token=" in response.headers["set-cookie"]


def test_login_with_name_returns_token(client, created_user):
    response = client.post(
        "/login",
        json={"login": created_user.name, "password": "secret123"},
    )

    assert response.status_code == 200
    assert response.json()["access_token"]


def test_login_rejects_invalid_credentials(client, created_user):
    response = client.post(
        "/login",
        json={"login": created_user.email, "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_me_returns_current_user_from_cookie_auth(client, created_user):
    client.post(
        "/login",
        json={"login": created_user.email, "password": "secret123"},
    )

    response = client.get("/me")

    assert response.status_code == 200
    assert response.json()["id"] == created_user.id
    assert response.json()["email"] == created_user.email


def test_me_requires_authentication(client):
    response = client.get("/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
