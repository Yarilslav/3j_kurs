from __future__ import annotations

from app.api.deps import get_current_user, get_optional_current_user, get_staff_or_admin_user


def test_create_guest_order(client, seeded_product):
    response = client.post(
        "/orders/",
        json={
            "items": [{"product_id": seeded_product.id, "quantity": 2}],
            "address": "Kyiv, Test street 1",
            "guest_name": "Tea Guest",
            "guest_contact": "+380501234567",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert response.json()["total_price"] == seeded_product.price_uah * 2
    assert response.json()["guest_name"] == "Tea Guest"
    assert response.json()["what_ordered"] == f"{seeded_product.name} x2"


def test_create_order_requires_guest_contact_for_guest(client, seeded_product):
    response = client.post(
        "/orders/",
        json={
            "items": [{"product_id": seeded_product.id, "quantity": 1}],
            "guest_name": "Tea Guest",
        },
    )

    assert response.status_code == 422


def test_create_authenticated_order_uses_current_user(client, created_user, seeded_product):
    app = client.app
    app.dependency_overrides[get_optional_current_user] = lambda: created_user

    response = client.post(
        "/orders/",
        json={
            "items": [{"product_id": seeded_product.id, "quantity": 1}],
            "guest_name": "Ignored Guest",
            "guest_contact": "Ignored Contact",
        },
    )

    assert response.status_code == 201
    assert response.json()["user_id"] == created_user.id
    assert response.json()["guest_name"] is None


def test_get_orders_returns_only_current_user_orders(client, created_user, seeded_product):
    app = client.app
    app.dependency_overrides[get_optional_current_user] = lambda: created_user
    app.dependency_overrides[get_current_user] = lambda: created_user

    client.post(
        "/orders/",
        json={"items": [{"product_id": seeded_product.id, "quantity": 1}]},
    )

    response = client.get("/orders/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["user_id"] == created_user.id


def test_update_order_status_requires_staff_role(client, seeded_product):
    create_response = client.post(
        "/orders/",
        json={
            "items": [{"product_id": seeded_product.id, "quantity": 1}],
            "guest_name": "Tea Guest",
            "guest_contact": "+380501234567",
        },
    )

    response = client.patch(
        f"/orders/{create_response.json()['id']}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 401


def test_staff_can_update_order_status(client, staff_user, seeded_product):
    create_response = client.post(
        "/orders/",
        json={
            "items": [{"product_id": seeded_product.id, "quantity": 1}],
            "guest_name": "Tea Guest",
            "guest_contact": "+380501234567",
        },
    )

    app = client.app
    app.dependency_overrides[get_staff_or_admin_user] = lambda: staff_user

    response = client.patch(
        f"/orders/{create_response.json()['id']}/status",
        json={"status": "confirmed"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"
