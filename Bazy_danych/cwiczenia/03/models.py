from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()



class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    country = Column(String(length=50))

    written_books = relationship("Book", back_populates="book_author", cascade="all, delete-orphan")




class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=50), nullable=False)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))

    book_author = relationship("Author", back_populates="written_books")
    
