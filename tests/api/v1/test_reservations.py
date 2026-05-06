from __future__ import annotations

from app.api.deps import get_current_user, get_optional_current_user, get_staff_or_admin_user


def test_create_guest_reservation(client):
    response = client.post(
        "/reservations/",
        json={
            "reservation_at": "2026-05-10 18:00",
            "places": [1, 2, 3],
            "guest_name": "Tea Guest",
            "guest_contact": "+380501234567",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert response.json()["price"] == 0
    assert response.json()["places"] == [1, 2, 3]


def test_create_authenticated_reservation_uses_current_user(client, created_user):
    app = client.app
    app.dependency_overrides[get_optional_current_user] = lambda: created_user

    response = client.post(
        "/reservations/",
        json={
            "reservation_at": "2026-05-10 18:00",
            "places": "4,5",
        },
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == created_user.id
    assert response.json()["places"] == [4, 5]


def test_get_reservations_returns_only_current_user_reservations(client, created_user):
    app = client.app
    app.dependency_overrides[get_optional_current_user] = lambda: created_user
    app.dependency_overrides[get_current_user] = lambda: created_user

    client.post(
        "/reservations/",
        json={"reservation_at": "2026-05-10 18:00", "places": [1]},
    )

    response = client.get("/reservations/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == created_user.id


def test_update_reservation_status_requires_staff_role(client):
    create_response = client.post(
        "/reservations/",
        json={
            "reservation_at": "2026-05-10 18:00",
            "places": [1],
            "guest_name": "Tea Guest",
            "guest_contact": "+380501234567",
        },
    )

    response = client.patch(
        f"/reservations/{create_response.json()['id']}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 401


def test_staff_can_update_reservation_status(client, staff_user):
    create_response = client.post(
        "/reservations/",
        json={
            "reservation_at": "2026-05-10 18:00",
            "places": [1],
            "guest_name": "Tea Guest",
            "guest_contact": "+380501234567",
        },
    )

    app = client.app
    app.dependency_overrides[get_staff_or_admin_user] = lambda: staff_user

    response = client.patch(
        f"/reservations/{create_response.json()['id']}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"
