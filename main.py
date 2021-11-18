import uvicorn
from fastapi import FastAPI

from routes import router
from config import database

app = FastAPI()

app.state.database = database

app.include_router(router, prefix='')

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
