from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# User
class UserBase(BaseModel):
    user_name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    date_registered: Optional[datetime]

    class Config:
        crm_mode = True


class UserResponse(UserInDB):
    pass


# Product
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


# Order
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
