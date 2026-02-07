from models import Base, Room, Guest, Reservation
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func
from datetime import date


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Zadanie 1: Dodaj pokoje i gosci."""
    # TODO: Utworz pokoje i gosci
    pass


def check_availability(session, room_id, check_in, check_out):
    """Zadanie 3: Sprawdz czy pokoj jest dostepny."""
    # TODO: Sprawdz kolizje z istniejacymi rezerwacjami
    # Kolizja: istniejaca.check_in < new.check_out AND istniejaca.check_out > new.check_in
    pass


def make_reservation(session, guest_id, room_id, check_in, check_out):
    """Zadanie 2: Utworz rezerwacje z walidacja i transakcja."""
    # TODO: Sprawdz walidacje (daty, dostepnosc)
    # TODO: Oblicz cene
    # TODO: Utworz rezerwacje w transakcji
    # TODO: W razie bledu -> rollback
    pass


def cancel_reservation(session, reservation_id):
    """Zadanie 4: Anuluj rezerwacje."""
    # TODO: Zmien status na "anulowana" w transakcji
    pass


def active_reservations(session):
    """Zadanie 5a: Lista aktywnych rezerwacji."""
    # TODO: Filtruj po statusie
    pass


def monthly_revenue(session, year, month):
    """Zadanie 5b: Przychod w danym miesiacu."""
    # TODO: Filtruj po dacie i sumuj total_price
    pass


def most_popular_room(session):
    """Zadanie 5c: Pokoj z najwieksza liczba rezerwacji."""
    # TODO: Uzyj group_by z func.count
    pass


def top_guest(session):
    """Zadanie 5d: Gosc z najwyzsza kwota."""
    # TODO: Uzyj func.sum z order_by
    pass


if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            # TODO: Wywolaj funkcje w odpowiedniej kolejnosci
            pass
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Blad bazy danych: {e}")
