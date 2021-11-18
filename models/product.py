import ormar
from fastapi import HTTPException, status
from pydantic import validator

from config import database, metadata


class Product(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255)
    price: float = ormar.Float()
    stock: int = ormar.Integer()

    @validator('price')
    def has_valid_price(cls, property_value):
        if not property_value >= 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Product price must be positive')
        return property_value
