from typing import List
from fastapi import APIRouter, HTTPException, status, Response

from models.product import Product

router = APIRouter(prefix='/product')


@router.get('', response_model=List[Product])
async def list_products():
    return await Product.objects.all()


@router.post('', response_model=Product)
async def create_product(product: Product, response: Response):
    await product.save()
    response.status_code=status.HTTP_201_CREATED
    return product


@router.delete('/{product_id}')
async def delete_product(product_id: int, response: Response):
    product = await Product.objects.get_or_none(id=product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    await product.delete()
    response.status_code = status.HTTP_200_OK
