from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


# TODO: Zdefiniuj model Customer
# Kolumny: id, name, email (UNIQUE), city
# Relacja: orders (1:N)

class Customer(Base):
    __tablename__ = "customers"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Product
# Kolumny: id, name, price, category
# Relacja: orders (1:N)

class Product(Base):
    __tablename__ = "products"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Order
# Kolumny: id, customer_id (FK), product_id (FK), quantity, order_date
# Relacje: customer, product (back_populates)

class Order(Base):
    __tablename__ = "orders"

    # Tutaj zdefiniuj kolumny i relacje
    pass
