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


def test_update_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post("/products", json=product_mock)
    content = response.json()
    #
    product_id = content.pop('id')
    content['name'] = 'edited'
    content['price'] = 0.5
    content['stock'] = 4
    response = client.put('/products/' + str(product_id), json=content)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['name'] == 'edited'
    assert content['price'] == 0.5
    assert content['stock'] == 4


def test_delete_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post("/products", json=product_mock)
    content = response.json()
    product_id = content.pop('id')
    response = client.delete('/products/' + str(product_id) )
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/products")
    content = response.json()
    assert content['total'] == 0
