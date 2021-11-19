from fastapi.testclient import TestClient
from fastapi import status

from tests.mocks.products import create_valid_product


def test_list_products(client: TestClient) -> None:
    response = client.get('/products?limit=2')
    content = response.json()
    assert content['per_page'] == 2
    assert len(content['data']) == 0
    assert response.status_code == status.HTTP_200_OK


def test_create_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post('/products', json=product_mock)
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert content['name'] == product_mock['name']


def test_get_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post('/products', json=product_mock)
    created_product = response.json()
    response = client.get('/products/' + str(created_product['id']))
    retrieved_product = response.json()
    assert created_product['id'] == retrieved_product['id']
    assert created_product['name'] == retrieved_product['name']
    assert created_product['price'] == retrieved_product['price']
    assert created_product['stock'] == retrieved_product['stock']


def test_update_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post('/products', json=product_mock)
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
    response = client.post('/products', json=product_mock)
    content = response.json()
    product_id = content.pop('id')
    response = client.delete('/products/' + str(product_id))
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/products')
    content = response.json()
    assert content['total'] == 0


def test_get_total_stock_price(client: TestClient) -> None:
    products_amount = 2
    for i in range(products_amount):
        product_mock = create_valid_product()
        response = client.post('/products', json=product_mock)
    response = client.get('/products/stock-price')
    content = response.json()
    product_mock = create_valid_product()
    assert content['stock_price'] == product_mock['price'] * product_mock['stock'] * products_amount
    assert content['stock_amount'] == products_amount * product_mock['stock']