import logging

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.persistence.database import get_db
from app.schemas.order_schema import *
from app.service import order_service

router = APIRouter(
        prefix="/v1/orders",
        tags=["Order"]
)


# Order
@router.post(path="", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    logging.info(f"create order: {order.model_dump_json()}")
    return order_service.create_order(db=db, order=order)


@router.get(path="/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    logging.info(f"get order by id: {order_id}")

    db_order = order_service.get_order_by_id(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found.")

    return db_order


@router.get(path="", response_model=List[OrderResponse])
def get_orders(offset: int, limit: int, db: Session = Depends(get_db)):
    logging.info(f"get orders, offset: {offset}, limit: {limit}")
    return order_service.get_orders(db, skip=offset, limit=limit)


@router.put(path="/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    logging.info(f"update order: {order_id}, order: {order.model_dump_json()}")
    return order_service.update_order(db, order_id, updated_data=order)
