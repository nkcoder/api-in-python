from sqlalchemy.orm import Session

from persistence.models import Product
from schemas.product_schema import ProductCreate, ProductUpdate


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
