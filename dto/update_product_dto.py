from typing import Optional

from pydantic import BaseModel


class UpdateProductDto(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    def to_dict(self):
        return vars(self)
