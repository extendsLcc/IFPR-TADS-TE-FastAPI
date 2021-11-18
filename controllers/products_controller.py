from typing import List
from fastapi import APIRouter

from models.product import Product

router = APIRouter(prefix='/product')


@router.get('', response_model=List[Product])
async def list_products():
    return await Product.objects.all()


@router.post('', response_model=Product)
async def create_product(product: Product):
    await product.save()
    return product
