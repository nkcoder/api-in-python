from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    seller_id: int
    product_name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


class ProductInDB(ProductBase):
    id: int

    class Config:
        orm_mode = True


class ProductResponse(ProductInDB):
    pass
