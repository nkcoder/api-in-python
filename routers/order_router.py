import logging
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
        prefix="/v1/orders",
        tags=["Order"]
)


# Order
@router.post(path="", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    logging.info(f"create order: {order.model_dump_json()}")
    return crud.create_order(db=db, order=order)


@router.get(path="/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    logging.info(f"get order by id: {order_id}")

    db_order = crud.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found.")

    return db_order


@router.get(path="", response_model=List[schemas.OrderResponse])
def get_orders(offset: int, limit: int, db: Session = Depends(get_db)):
    logging.info(f"get orders, offset: {offset}, limit: {limit}")
    return crud.get_orders(db, skip=offset, limit=limit)


@router.put(path="/{order_id}", response_model=schemas.OrderResponse)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    logging.info(f"update order: {order_id}, order: {order.model_dump_json()}")
    return crud.update_order(db, order_id, updated_data=order)
