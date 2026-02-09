from models import Base, Contact
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError


def clear_table(session):
    create_tables()
    session.query(Contact).delete()
    session.commit()


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)
    


def add_contacts(session):
    """Zadanie 2: Dodaj co najmniej 5 kontaktow."""
    # TODO: Utwórz obiekty Contact i dodaj do sesji
    contacts = [
            Contact(first_name="Jan", last_name="Kowalski", email="janK.@example.pl", phone="123-456-789"),
            Contact(first_name="Ala", last_name="Goś", email="AlaG@example.pl"),
            Contact(first_name="Ola", last_name="Babola", email="OlaB@qq.com"),
            Contact(first_name="Hanna", last_name="Wanna", email="HaN@ha.pl", phone="235-567-951"),
            Contact(first_name="Monika", last_name="Słoń", email="MoniaM@mon.com"),
        ]
    session.add_all(contacts)
    session.commit()
    print("Załadowano 5 kontaktów")


def show_all_contacts(session):
    """Zadanie 3a: Wyświetl wszystkie kontakty."""
    # TODO: Pobierz wszystkie kontakty i wyświetl
    contacts = session.query(Contact).all()
    for contact in contacts:
        print(contact.first_name)


def find_by_email(session, email):
    """Zadanie 3b: Znajdź kontakt po emailu."""
    # TODO: Użyj filter_by do wyszukania po emailu
    result = session.query(Contact).filter_by(email=email).first()
    if result:
        print(result.first_name, result.email)


def find_by_last_name(session, last_name):
    """Zadanie 3c: Znajdź kontakty po nazwisku."""
    # TODO: Użyj filter_by do wyszukania po nazwisku
    results = session.query(Contact).filter_by(last_name=last_name).all()
    for result in results:
        print(result.first_name, result.last_name)


def update_phone(session, email, new_phone):
    """Zadanie 4a: Zmień numer telefonu kontaktu."""
    # TODO: Znajdź kontakt i zaktualizuj telefon
    result = session.query(Contact).filter_by(email=email).first()
    if result:
        result.phone = new_phone   
        session.commit()
        print(f"telefon dla {result.first_name}, {result.email} został dodany/zmieniony na {result.phone}")
    else:
        print("Nie znaleziono kontaktu")


def update_email(session, old_email, new_email):
    """Zadanie 4b: Zmień email kontaktu."""
    # TODO: Znajdź kontakt i zaktualizuj email
    result = session.query(Contact).filter_by(email=old_email).first()
    if result:
        result.email = new_email
        session.commit()
        print(f"Email dla kontaktu {result.first_name}, {old_email} został zmieniony na {result.email}")
    else:
        print("Nie znaleziono kontaktu")
      


def delete_by_id(session, contact_id):
    """Zadanie 5a: Usuń kontakt po ID."""
    # TODO: Znajdź kontakt po ID i usuń
    contacts = session.query(Contact).all()
    for contact in contacts:
        print(f"Przed: {contact.first_name}")

    result = session.query(Contact).filter_by(id=contact_id).first()
    if result:
        session.delete(result)
        session.commit()    
        print(f"\nKontakt {result.first_name}, numer id: {result.id} - został usunięty\n")
    else:
        print("Nie znaleziono kontaktu")

    contacts = session.query(Contact).all()
    for contact in contacts:
        print(f"PO: {contact.first_name}")

    # Czy tutaj bardziej precyzyjnym rozwiązaniem nie było by porownanie ilości wpisów przed i po? - pytanie do Kludiusza.


def delete_by_email(session, email):
    """Zadanie 5b: Usuń kontakt po emailu."""
    # TODO: Znajdź kontakt po emailu i usuń
    result = session.query(Contact).filter_by(email=email).first()
    if result:
        session.delete(result)
        session.commit()
    else:
        print("Nie znaleziono kontaktu")

    print("\n")
    contacts = session.query(Contact).all()
    for contact in contacts:
        print(f"PO: {contact.first_name}")





if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            # TODO: Wywołaj funkcję w odpowiedniej kolejności
            clear_table(session)
            add_contacts(session)
            print("\n")
            show_all_contacts(session)
            print("\n")
            find_by_email(session, "MoniaM@mon.com")
            print("\n")
            find_by_last_name(session, "Babola")
            print("\n")
            update_phone(session, "MoniaM@mon.com", "123-456-789")
            print("\n")
            update_email(session, "AlaG@example.pl", "GAla@example.com.pl")
            print("\n")
            delete_by_id(session, 1)
            print("\n")
            delete_by_email(session, "HaN@ha.pl")

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
