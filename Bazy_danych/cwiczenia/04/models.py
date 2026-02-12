from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# TODO: Zdefiniuj model Category
# Kolumny: id, name
# Relacja: products (1:N)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False, unique=True)

    category_rel = relationship("Product", back_populates="products_rel", cascade="all, delete-orphan")

# TODO: Zdefiniuj model Product
# Kolumny: id, name, price, quantity, category_id

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))

    products_rel = relationship("Category", back_populates="category_rel")