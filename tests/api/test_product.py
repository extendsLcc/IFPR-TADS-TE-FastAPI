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


def test_create_product_validation(client: TestClient) -> None:
    product_mock = create_valid_product()
    product_mock['price'] = -1
    response = client.post('/products', json=product_mock)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


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


def test_get_product_404(client: TestClient) -> None:
    response = client.get('/products/1')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post('/products', json=product_mock)
    content = response.json()
    #
    product_id = content.pop('id')
    content['name'] = 'edited'
    content['price'] = 0.5
    content['stock'] = 4
    response = client.put(f'/products/{product_id}', json=content)
    content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert content['name'] == 'edited'
    assert content['price'] == 0.5
    assert content['stock'] == 4


def test_update_product_404(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.put('/products/1', json=product_mock)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_product(client: TestClient) -> None:
    product_mock = create_valid_product()
    response = client.post('/products', json=product_mock)
    content = response.json()
    product_id = content.pop('id')
    response = client.delete(f'/products/{product_id}')
    assert response.status_code == status.HTTP_200_OK
    response = client.get('/products')
    content = response.json()
    assert content['total'] == 0


def test_get_total_stock_price(client: TestClient) -> None:
    products_amount = 2
    for i in range(products_amount):
        product_mock = create_valid_product()
        client.post('/products', json=product_mock)
    response = client.get('/products/stock-price')
    content = response.json()
    product_mock = create_valid_product()
    assert content['stock_price'] == product_mock['price'] * product_mock['stock'] * products_amount
    assert content['stock_amount'] == products_amount * product_mock['stock']


def test_list_products_filter(client: TestClient) -> None:
    products_amount = 3
    search_name = '1'
    for index in range(products_amount):
        product_mock = create_valid_product()
        product_mock['name'] += f' {index}'
        client.post('/products', json=product_mock)
    response = client.get(f'/products?name={search_name}')
    content = response.json()
    products = content['data']
    first_result = next(iter(products))
    assert search_name in first_result['name']


def test_list_products_pagination(client: TestClient) -> None:
    products_amount = 9
    limit = 3
    page = 2
    for index in range(products_amount):
        product_mock = create_valid_product()
        product_mock['name'] += f' {index}'
        client.post('/products', json=product_mock)
    response = client.get(f'/products?limit={limit}&page={page}')
    content = response.json()
    assert content['page'] == page
    assert content['per_page'] == limit
    assert content['total'] == products_amount
    products = content['data']
    assert len(products) == limit
    for index, product in enumerate(products):
        assert str(limit + index) in product['name']
