from sqlalchemy.orm import Session

from app.models import Product


def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, updated_product: Product):
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    for var, value in vars(updated_product).items():
        setattr(existing_product, var, value)
    db.commit()
    return existing_product


def delete_product(db: Session, product_id: int):
    product_to_delete = db.query(Product).filter(Product.id == product_id).first()
    db.delete(product_to_delete)
    db.commit()
