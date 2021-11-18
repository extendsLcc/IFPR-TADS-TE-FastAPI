import ormar
from config import database, metadata


class Product(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255)
    price: float = ormar.Float()
    stock: int = ormar.Integer()

    def has_valid_price(self):
        return self.price >= 0
