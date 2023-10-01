import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
        prefix="/v1/products",
        tags=['Product']
)

logger = logging.getLogger("order router")


# Product
@router.post(path="", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"create product: {product.model_dump_json()}")
    return crud.create_product(db=db, product=product)


@router.get(path="/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    logger.info(f"get product by id: {product_id}")

    db_product = crud.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")

    return db_product


@router.get(path="", response_model=List[schemas.ProductResponse])
def get_products(offset: int, limit: int, db: Session = Depends(get_db)):
    logger.info(f"get products, offset: {offset}, limit: {limit}")
    return crud.get_products(db, skip=offset, limit=limit)


@router.put(path="/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    logger.info(f"update product: {product_id}, product: {product.model_dump_json()}")
    return crud.update_product(db, product_id, updated_data=product)
