from fastapi.testclient import TestClient
from fastapi import status

from tests.mocks.products import create_valid_product


def test_empty_paginated_products(client: TestClient) -> None:
    response = client.get("/products?limit=2")
    content = response.json()
    assert content['per_page'] == 2
    assert len(content['data']) == 0
    assert response.status_code == status.HTTP_200_OK


def test_create_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post("/products", json=product_mock)
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert content['name'] == product_mock['name']