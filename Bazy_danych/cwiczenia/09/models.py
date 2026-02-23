from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# TODO: Zdefiniuj model Room
# Kolumny: id, name, capacity, price_per_night, is_available

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

    reservations = relationship("Reservation", back_populates="room", cascade="all, delete-orphan")

# TODO: Zdefiniuj model Guest
# Kolumny: id, name, email (UNIQUE), phone

class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False, unique=True)
    phone = Column(String(length=20))

    reservations = relationship("Reservation", back_populates="guest", cascade="all, delete-orphan")

# TODO: Zdefiniuj model Reservation
# Kolumny: id, guest_id (FK), room_id (FK), check_in, check_out, total_price, status

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    guest_id = Column(Integer, ForeignKey("guests.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(length=20), default="potwierdzona")

    room = relationship("Room", back_populates="reservations")
    guest = relationship("Guest", back_populates="reservations")