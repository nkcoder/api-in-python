from typing import List, Optional

from pydantic import BaseModel

from .product_schema import ProductInDB


class ProductInOrder(BaseModel):
    product_id: int
    quantity: int


class OrderBase(BaseModel):
    buyer_id: int
    total_amount: float
    shipping_address_id: int


class OrderCreate(OrderBase):
    product_ids: List[int]


class OrderUpdate(BaseModel):
    total_amount: Optional[float] = None
    shipping_address_id: Optional[int] = None,
    product_ids: List[int]


class OrderInDB(OrderBase):
    id: int
    products: List[ProductInDB]

    class Config:
        orm_mode = True


class OrderResponse(OrderInDB):
    pass
