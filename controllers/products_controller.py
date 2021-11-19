from typing import Optional
from fastapi import APIRouter, HTTPException, status, Response
from functools import reduce

from dto.paginated_set import PaginatedSet
from dto.update_product_dto import UpdateProductDto
from models.product import Product

router = APIRouter(prefix='/products')


@router.get('', response_model=PaginatedSet)
async def list_products(name: Optional[str] = None, page: Optional[int] = 1, limit: Optional[int] = 5):
    if name:
        paginated_results = await Product.objects.filter(
            Product.name.icontains(name)
        ) \
            .paginate(page) \
            .limit(limit) \
            .all()
    else:
        paginated_results = await Product.objects \
            .paginate(page) \
            .limit(limit) \
            .all()
    total_products = await Product.objects.count()
    return PaginatedSet(
        data=paginated_results,
        page=page,
        per_page=limit,
        total=total_products,
    )


@router.post('', response_model=Product)
async def create_product(product: Product, response: Response):
    await product.save()
    response.status_code = status.HTTP_201_CREATED
    return product


@router.put('/{product_id}')
async def update_product(product_id: int, update_product_dto: UpdateProductDto):
    product = await Product.objects.get_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    filled_update_properties = dict(
        (prop, value) for (prop, value) in update_product_dto.to_dict().items() if value is not None
    )
    for prop, value in filled_update_properties.items():
        setattr(product, prop, value)
    updated_columns_names = filled_update_properties.keys()
    await product.update(_columns=updated_columns_names)
    return product


@router.delete('/{product_id}')
async def delete_product(product_id: int):
    product = await Product.objects.get_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    await product.delete()


@router.get('/stock-price')
async def get_total_stock_price():
    products = await Product.objects.all()
    return {
        'stock_price': reduce(lambda total_price, product: total_price + product.price * product.stock, products, 0),
        'stock_amount': reduce(lambda total_stock, product: total_stock + product.stock, products, 0),
    }
