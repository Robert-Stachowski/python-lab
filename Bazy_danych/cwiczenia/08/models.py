from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# TODO: Zdefiniuj model Customer
# Kolumny: id, name, email (UNIQUE), city
# Relacja: orders (1:N)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False, unique=True)
    city = Column(String(length=100), nullable=False)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


# TODO: Zdefiniuj model Product
# Kolumny: id, name, price, category
# Relacja: orders (1:N)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=200), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(length=50), nullable=False)

    orders = relationship("Order", back_populates="product", cascade="all, delete-orphan")

    

# TODO: Zdefiniuj model Order
# Kolumny: id, customer_id (FK), product_id (FK), quantity, order_date
# Relacje: customer, product (back_populates)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")