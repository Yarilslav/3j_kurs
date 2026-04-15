from __future__ import annotations


def test_get_products_returns_empty_list(client):
    response = client.get("/products/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_products_returns_seeded_products(client, seeded_product):
    response = client.get("/products/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == seeded_product.name
