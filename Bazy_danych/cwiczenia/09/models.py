from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# TODO: Zdefiniuj model Room
# Kolumny: id, name, capacity, price_per_night, is_available

class Room(Base):
    __tablename__ = "rooms"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Guest
# Kolumny: id, name, email (UNIQUE), phone

class Guest(Base):
    __tablename__ = "guests"

    # Tutaj zdefiniuj kolumny i relacje
    pass


# TODO: Zdefiniuj model Reservation
# Kolumny: id, guest_id (FK), room_id (FK), check_in, check_out, total_price, status

class Reservation(Base):
    __tablename__ = "reservations"

    # Tutaj zdefiniuj kolumny i relacje
    pass
