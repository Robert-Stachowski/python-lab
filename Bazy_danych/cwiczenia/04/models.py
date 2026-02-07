from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# TODO: Zdefiniuj model Category
# Kolumny: id, name
# Relacja: products (1:N)

class Category(Base):
    __tablename__ = "categories"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Product
# Kolumny: id, name, price, quantity, category_id

class Product(Base):
    __tablename__ = "products"

    # Tutaj zdefiniuj kolumny i relacje
    pass
