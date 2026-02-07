from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# TODO: Zdefiniuj model Movie
# Kolumny: id, title, director, year, genre, rating

class Movie(Base):
    __tablename__ = "movies"

    # Tutaj zdefiniuj kolumny
    pass
