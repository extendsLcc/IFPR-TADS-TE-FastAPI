from typing import List

from pydantic import BaseModel


class PaginatedSet(BaseModel):
    page: int
    per_page: int
    total: int
    data: List[dict] = []
