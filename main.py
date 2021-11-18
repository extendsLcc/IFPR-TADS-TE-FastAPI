from fastapi import FastAPI

from routes import router
from config import database

app = FastAPI()

app.state.database = database

app.include_router(router,prefix='')