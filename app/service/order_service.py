from sqlalchemy.orm import Session

from app.persistence.models import Order, Product
from app.schemas.order_schema import OrderCreate, OrderUpdate


def create_order(db: Session, order: OrderCreate):
    products = db.query(Product).filter(Product.id.in_(order.product_ids)).all()
    db_order = Order(
            buyer_id=order.buyer_id,
            total_amount=order.total_amount,
            shipping_address_id=order.shipping_address_id,
            products=products
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def delete_order(db: Session, order_id: int):
    order = get_order_by_id(order_id)
    db.delete(order)
    db.commit()


def update_order(db: Session, order_id: int, updated_data: OrderUpdate):
    db_order = db.query(Order).filter(Order.id == order_id).one()
    updated_data_dict = updated_data.model_dump(exclude_unset=True, exclude={"product_ids"})
    for key, value in updated_data_dict.items():
        setattr(db_order, key, value)

    if updated_data.product_ids:
        products = db.query(Product).filter(Product.id.in_(updated_data.product_ids)).all()
        db_order.products = products

    db.commit()
    db.refresh(db_order)
    return get_order_by_id(db, order_id)
