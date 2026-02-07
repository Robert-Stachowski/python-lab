from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from datetime import date

Base = declarative_base()


# TODO: Zdefiniuj model Workout
# Kolumny: id, name, workout_type, duration_minutes, calories, date
# Pamietaj o default=date.today dla kolumny date

class Workout(Base):
    __tablename__ = "workouts"

    # Tutaj zdefiniuj kolumny
    pass
