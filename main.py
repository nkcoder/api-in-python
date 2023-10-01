import logging

from fastapi import FastAPI

from routers import user_router, order_router, product_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(order_router.router)
app.include_router(product_router.router)

logging = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"message": "Your API is working!"}
