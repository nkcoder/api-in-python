from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import User, Product, Order
from app.schemas import ProductCreate, UserCreate, OrderCreate, OrderUpdate, UserUpdate, \
    ProductUpdate


# User
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.user_name == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, updated_data: UserUpdate):
    db.query(User).filter(User.id == user_id).update(updated_data.model_dump(exclude_unset=True))
    db.commit()
    return get_user_by_id(db, user_id)


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = user.password + "faked_hash"
    db_user = User(user_name=user.user_name, email=user.email,
                   password=hashed_password,
                   date_registered=func.now())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Product
def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(
            seller_id=product.seller_id,
            product_name=product.product_name,
            description=product.description,
            price=product.price,
            quantity=product.quantity
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    product_id = get_product_by_id(db, product_id)
    db.delete(product_id)
    db.commit()


def update_product(db: Session, product_id: int, updated_data: ProductUpdate):
    db.query(Product).filter(Product.id == product_id).update(
            updated_data.model_dump(exclude_unset=True));
    db.commit()
    return get_product_by_id(db, product_id)


# Order
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
