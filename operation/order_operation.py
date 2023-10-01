from typing import List

from sqlalchemy.orm import Session

from app.models import Order, Product


def create_order(db: Session, order: Order, product_ids: List[int]):
    order.products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order_by_id(db: Session, order_id: int) -> Order:
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, updated_order: Order):
    existing_order = db.query(Order).filter(Order.id == order_id).first()
    for var, value in vars(updated_order).items():
        setattr(existing_order, var, value)
    db.commit()
    return existing_order


def delete_order(db: Session, order_id: int):
    order_to_delete = db.query(Order).filter(Order.id == order_id).first()
    db.delete(order_to_delete)
    db.commit()
