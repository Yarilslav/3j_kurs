from __future__ import annotations


def test_metrics_endpoint_exposes_prometheus_metrics(client):
    client.get("/")

    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
    assert "http_request_duration_seconds" in response.text


def test_metrics_endpoint_exposes_custom_counts(client, created_user, seeded_product):
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "users_total 1.0" in response.text
    assert "products_total 1.0" in response.text
