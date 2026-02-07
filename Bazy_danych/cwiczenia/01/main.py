from models import Base, Contact
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def add_contacts(session):
    """Zadanie 2: Dodaj co najmniej 5 kontaktow."""
    # TODO: Utworz obiekty Contact i dodaj do sesji
    pass


def show_all_contacts(session):
    """Zadanie 3a: Wyswietl wszystkie kontakty."""
    # TODO: Pobierz wszystkie kontakty i wyswietl
    pass


def find_by_email(session, email):
    """Zadanie 3b: Znajdz kontakt po emailu."""
    # TODO: Uzyj filter_by do wyszukania po emailu
    pass


def find_by_last_name(session, last_name):
    """Zadanie 3c: Znajdz kontakty po nazwisku."""
    # TODO: Uzyj filter_by do wyszukania po nazwisku
    pass


def update_phone(session, email, new_phone):
    """Zadanie 4a: Zmien numer telefonu kontaktu."""
    # TODO: Znajdz kontakt i zaktualizuj telefon
    pass


def update_email(session, old_email, new_email):
    """Zadanie 4b: Zmien email kontaktu."""
    # TODO: Znajdz kontakt i zaktualizuj email
    pass


def delete_by_id(session, contact_id):
    """Zadanie 5a: Usun kontakt po ID."""
    # TODO: Znajdz kontakt po ID i usun
    pass


def delete_by_email(session, email):
    """Zadanie 5b: Usun kontakt po emailu."""
    # TODO: Znajdz kontakt po emailu i usun
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
