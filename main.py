from typing import List

from fastapi import FastAPI, Response, status
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    descricao: str
    quantidade: int
    valor: float


app = FastAPI()

items: List[Item] = []


@app.get("/items")
def index_items():
    return items


@app.post("/items")
def add_item(item: Item):
    items.append(item)
    return item


@app.get("/items/valor-total")
def get_valor_total():
    valor_total = sum([item.valor * item.quantidade for item in items])
    return {"valor_total": valor_total}


@app.get("/items/{item_id}")
def read_item(item_id: int, response: Response):
    if not any(item.id == item_id for item in items):
        response.status_code = status.HTTP_404_NOT_FOUND
    return next((item for item in items if item.id == item_id), None)


@app.delete("/items/{item_id}")
def delete_item(item_id: int, response: Response):
    global items
    if not any(item.id == item_id for item in items):
        response.status_code = status.HTTP_404_NOT_FOUND
    items = [item for item in items if item.id != item_id]
