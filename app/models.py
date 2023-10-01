from sqlalchemy import Column, Integer, DateTime, Double, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

order_products_association = Table(
        "order_products",
        Base.metadata,
        Column("order_id", Integer, ForeignKey("orders.id")),
        Column("product_id", Integer, ForeignKey("products.id"))
)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"))
    date_placed = Column(DateTime(timezone=True))
    total_amount = Column(Double, nullable=False)
    shipping_address_id = Column(Integer)
    products = relationship("Product", secondary=order_products_association,
                            back_populates="orders")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    date_registered = Column(DateTime(timezone=True))


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Double, nullable=False)
    quantity = Column(Integer, nullable=False)
    orders = relationship("Order", secondary=order_products_association, back_populates="products")
