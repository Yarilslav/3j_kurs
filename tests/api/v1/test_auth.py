from __future__ import annotations


def test_register_creates_user(client):
    response = client.post(
        "/register",
        json={
            "name": "Test",
            "email": "Test@example.com",
            "login": "test-login",
            "phone_number": "+380501234567",
            "password": "123456",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "Test@example.com"
    assert response.json()["login"] == "test-login"
    assert response.json()["phone_number"] == "+380501234567"
    assert response.json()["role"] == "user"
    assert response.json()["view_history"] is None
    assert response.json()["purchase_history"] is None
    assert response.json()["about_employee"] is None


def test_register_rejects_internal_profile_fields(client):
    response = client.post(
        "/register",
        json={
            "name": "Test",
            "email": "Test@example.com",
            "login": "test-login",
            "password": "123456",
            "view_history": "manual value",
            "purchase_history": "manual value",
            "about_employee": "manual value",
        },
    )

    assert response.status_code == 422


def test_register_rejects_duplicate_email(client, created_user):
    response = client.post(
        "/register",
        json={
            "name": "Inshyj User",
            "email": created_user.email,
            "login": "another-login",
            "password": "123456",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_rejects_duplicate_login(client, created_user):
    response = client.post(
        "/register",
        json={
            "name": "Inshyj User",
            "email": "new@example.com",
            "login": created_user.login,
            "password": "123456",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Login already registered"


def test_login_with_login_returns_token_and_cookie(client, created_user):
    response = client.post(
        "/login",
        json={"login": created_user.login, "password": "123456"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]
    assert "access_token=" in response.headers["set-cookie"]


def test_login_rejects_invalid_credentials(client, created_user):
    response = client.post(
        "/login",
        json={"login": created_user.login, "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_me_returns_current_user_from_cookie_auth(client, created_user):
    client.post(
        "/login",
        json={"login": created_user.login, "password": "123456"},
    )

    response = client.get("/me")

    assert response.status_code == 200
    assert response.json()["id"] == created_user.id
    assert response.json()["email"] == created_user.email
    assert response.json()["login"] == created_user.login
    assert response.json()["role"] == "user"


def test_me_requires_authentication(client):
    response = client.get("/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
