from __future__ import annotations


def test_create_post_requires_authentication(client):
    response = client.post(
        "/posts/",
        json={"title": "First post", "content": "Protected endpoint"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_post_creates_post_for_logged_in_user(client, created_user):
    client.post(
        "/login",
        json={"login": created_user.email, "password": "secret123"},
    )

    response = client.post(
        "/posts/",
        json={"title": "First post", "content": "Protected endpoint"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "First post"
    assert response.json()["content"] == "Protected endpoint"
    assert response.json()["user_id"] == created_user.id
