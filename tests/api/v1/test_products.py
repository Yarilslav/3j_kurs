from __future__ import annotations

from app.api.deps import get_staff_or_admin_user


def test_get_products_returns_empty_list(client):
    response = client.get("/products/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_products_returns_seeded_products(client, seeded_product):
    response = client.get("/products/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == seeded_product.name
    assert response.json()[0]["categories"] == ["Chinese"]


def test_get_product_by_id_returns_product(client, seeded_product):
    response = client.get(f"/products/{seeded_product.id}")

    assert response.status_code == 200
    assert response.json()["id"] == seeded_product.id


def test_create_product_requires_staff_or_admin(client):
    response = client.post(
        "/products/",
        json={
            "name": "Sencha",
            "kind": "green",
            "categories": ["Japanese"],
            "price_uah": 250,
            "stock_quantity": 5,
        },
    )

    assert response.status_code == 401


def test_staff_can_create_product(client, staff_user):
    app = client.app
    app.dependency_overrides[get_staff_or_admin_user] = lambda: staff_user

    response = client.post(
        "/products/",
        json={
            "name": "Sencha",
            "native_name": "煎茶",
            "image_filename": "Sphagnum.jpg",
            "kind": "green",
            "categories": "Japanese, Plantation",
            "description": "Fresh tea",
            "price_uah": 250,
            "stock_quantity": 5,
        },
    )

    assert response.status_code == 201
    assert response.json()["categories"] == ["Japanese", "Plantation"]
    assert response.json()["image_filename"] == "Sphagnum.jpg"
    assert response.json()["reviews"] is None


def test_staff_can_update_product(client, staff_user, seeded_product):
    app = client.app
    app.dependency_overrides[get_staff_or_admin_user] = lambda: staff_user

    response = client.put(
        f"/products/{seeded_product.id}",
        json={
            "price_uah": 400,
            "stock_quantity": 9,
            "categories": ["Chinese", "Oolong"],
        },
    )

    assert response.status_code == 200
    assert response.json()["price_uah"] == 400
    assert response.json()["stock_quantity"] == 9
    assert response.json()["categories"] == ["Chinese", "Oolong"]


def test_staff_can_delete_product(client, staff_user, seeded_product):
    app = client.app
    app.dependency_overrides[get_staff_or_admin_user] = lambda: staff_user

    response = client.delete(f"/products/{seeded_product.id}")

    assert response.status_code == 200
    assert response.json() == {"message": "deleted"}
