from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from datetime import date

Base = declarative_base()



class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=100), nullable=False)
    workout_type = Column(String(length=50), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    calories = Column(Integer)
    date = Column(Date, default=date.today, nullable=False)