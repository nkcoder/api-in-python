import logging
from typing import List

from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

app = FastAPI()

logging = logging.getLogger(__name__)


# User
@app.post(path="/v1/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logging.info(f"post /v1/users: {user.model_dump_json()}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get(path="/v1/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/users/{user_id}")

    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@app.get(path="/v1/users", response_model=List[schemas.UserResponse])
def get_users(offset: int, limit: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/users, offset: {offset}, limit: {limit}")
    return crud.get_users(db, skip=offset, limit=limit)


@app.put(path="/v1/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    logging.info(f"put /v1/users/{user_id}, user: {user.model_dump_json()}")
    return crud.update_user(db, user_id, updated_data=user)


# Product
@app.post(path="/v1/products", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    logging.info(f"post /v1/products: {product.model_dump_json()}")
    return crud.create_product(db=db, product=product)


@app.get(path="/v1/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/products/{product_id}")

    db_product = crud.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_product


@app.get(path="/v1/products", response_model=List[schemas.ProductResponse])
def get_products(offset: int, limit: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/products, offset: {offset}, limit: {limit}")
    return crud.get_products(db, skip=offset, limit=limit)


@app.put(path="/v1/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    logging.info(f"put /v1/products/{product_id}, product: {product.model_dump_json()}")
    return crud.update_product(db, product_id, updated_data=product)


# Order
@app.post(path="/v1/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    logging.info(f"post /v1/orders: {order.model_dump_json()}")
    return crud.create_order(db=db, order=order)


@app.get(path="/v1/orders/{order_id}", response_model=schemas.OrderResponse)
def get_product(order_id: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/orders/{order_id}")

    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found.")

    return db_order


@app.get(path="/v1/orders", response_model=List[schemas.OrderResponse])
def get_orders(offset: int, limit: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/orders, offset: {offset}, limit: {limit}")
    return crud.get_orders(db, skip=offset, limit=limit)


@app.put(path="/v1/orders/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    logging.info(f"put /v1/orders/{order_id}, order: {order.model_dump_json()}")
    return crud.update_order(db, order_id, updated_data=order)
