from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()




class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=200), nullable=False)
    director = Column(String(length=100), nullable=False)
    year = Column(Integer, nullable=False)
    genre = Column(String(length=50), nullable=False)
    rating = Column(Float, default=0)
