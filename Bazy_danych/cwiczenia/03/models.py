from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# TODO: Zdefiniuj model Author
# Kolumny: id, name, country
# Relacja: books (1:N z cascade)

class Author(Base):
    __tablename__ = "authors"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Book
# Kolumny: id, title, year, author_id (ForeignKey)
# Relacja: author (back_populates)

class Book(Base):
    __tablename__ = "books"

    # Tutaj zdefiniuj kolumny i relacje
    pass
