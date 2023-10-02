import logging

from fastapi import FastAPI

from app.api import user_api, order_api, product_api

app = FastAPI()
app.include_router(user_api.router)
app.include_router(order_api.router)
app.include_router(product_api.router)

logging = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Your API is working!"}
