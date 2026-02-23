import sys
sys.stdout.reconfigure(encoding='utf-8')
from models import Base, Room, Guest, Reservation
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func, desc, text
from datetime import date


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)

def clear_all_tables(session):
    create_tables()
    session.query(Reservation).delete()
    session.query(Room).delete()
    session.query(Guest).delete()
    session.execute(text("ALTER SEQUENCE rooms_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE guests_id_seq RESTART WITH 1"))
    session.execute(text("ALTER SEQUENCE reservations_id_seq RESTART WITH 1"))
    session.commit()


def seed_data(session):
    """Zadanie 1: Dodaj pokoje i gosci."""
    # TODO: Utwórz pokoje i gosci

    room_101 = Room(name="Pokój 101 - Standard", capacity=2, price_per_night=220.0, is_available=True)
    room_102 = Room(name="Pokój 102 - Twin", capacity=2, price_per_night=240.0, is_available=True)
    room_201 = Room(name="Pokój 201 - Family", capacity=4, price_per_night=380.0, is_available=True)
    room_301 = Room(name="Pokój 301 - Suite", capacity=3, price_per_night=320.0, is_available=True)
    room_501 = Room(name="Pokój 501 - Studio", capacity=4, price_per_night=620.0, is_available=False)
    
    session.add_all([room_101, room_102, room_201, room_301, room_501])

    guest_1 = Guest(name="Robert Nowak", email="robert.nowak@example.com", phone="+48 500 111 222")
    guest_2 = Guest(name="Anna Kowalska", email="anna.kowalska@example.com", phone="+48 501 222 333")
    guest_3 = Guest(name="Piotr Zieliński", email="piotr.zielinski@example.com", phone="+48 502 333 444")
    guest_4 = Guest(name="Kasia Wiśniewska", email="kasia.wisniewska@example.com", phone="+48 503 444 555")
    guest_5 = Guest(name="Tomasz Lewandowski", email="tomasz.lewandowski@example.com", phone="+48 504 555 666")

    session.add_all([guest_1, guest_2, guest_3, guest_4, guest_5])
    session.commit()
    print ("Klienci i pokoje dodane")
    

def make_reservation(session, guest_id, room_id, check_in, check_out):
    """Zadanie 2: Utwórz rezerwacje z walidacją i transakcja."""
    # TODO: Sprawdź walidacje (daty, dostepnosc)
    # TODO: Oblicz cene
    # TODO: Utwórz rezerwacje w transakcji
    # TODO: W razie bledu -> rollback


    try:
        # walidacją dostępności   
        #  
        room = session.query(Room).get(room_id)

        if not room:
            print(f"Nie znaleziono pokoju o ID={room_id}!")
            return
        if not room.is_available:
            print("Pokój wyłączony z użytku!")
            return
        

        
        # walidacją daty (czy jest kolizja)
        if check_out <= check_in:
            print("Błąd: data wymeldowania musi być PO dacie zameldowania!")
            return

        if not check_availability(session, room_id, check_in, check_out):
            print("Termin zajęty!")
            return
            
        # cena
        nights = (check_out - check_in).days
        total = (nights * room.price_per_night)

        # tworzenie rezerwacji
        reservation = Reservation(
            guest_id = guest_id,
            room_id = room_id,
            check_in = check_in,
            check_out = check_out,
            total_price = total,
            status = "potwierdzona"
        )

        session.add(reservation)
        session.commit()
        print(f"Rezerwacja utworzona! {nights} nocy * {room.price_per_night} zł = {total} zł")
      

    except SQLAlchemyError as e:
        session.rollback()
        print (f" Błąd: {e}")





def check_availability(session, room_id, new_check_in, new_check_out):
    """Zadanie 3: Sprawdź czy pokój jest dostępny."""
    # TODO: Sprawdź kolizje z istniejacymi rezerwacjami
    # Kolizja: istniejaca.check_in < new.check_out AND istniejaca.check_out > new.check_in
    collision = (
            session.query(Reservation)
            .filter(Reservation.room_id == room_id, Reservation.status != "anulowana",
                and_ (Reservation.check_in < new_check_out, Reservation.check_out > new_check_in )
                )
            .first()
            )
    
    if collision:
        print(f"ZAJĘTY! Kolizja z rezerwacją {collision.check_in} - {collision.check_out}")
        return False
    else:
        print("Pokój dostępny!")
        return True





def cancel_reservation(session, reservation_id):
    """Zadanie 4: Anuluj rezerwacje."""
    # TODO: Zmien status na "anulowana" w transakcji
   
    try:
        result = session.query(Reservation).filter(Reservation.id == reservation_id).first()
        if result:
            result.status = "anulowana"
            session.commit()
            print(f"Zmieniono status dla: {reservation_id} {result.room.name} na 'anulowana' ")
        else:
            print("Nie znaleziono rezerwacji...")

    except SQLAlchemyError as e:
        session.rollback()
        print(f" Błąd {e} ")





def active_reservations(session):
    """Zadanie 5a: Lista aktywnych rezerwacji."""
    # TODO: Filtruj po statusie
    
    result = session.query(Reservation).filter_by(status = "potwierdzona").all()
    for res in result:
        print(f"Rezerwacje aktywne: {res.guest.name}, {res.room.name}, {res.check_in} - {res.check_out}, {res.total_price} złotych")





def monthly_revenue(session, year, month):
    """Zadanie 5b: Przychód w danym miesiącu."""
    # TODO: Filtruj po dacie i sumuj total_price
    result = (
        session.query(func.sum(Reservation.total_price))
        .filter(
            func.extract('year', Reservation.check_in) == year,
            func.extract('month', Reservation.check_in) == month,
            Reservation.status != "anulowana"
            )
        .scalar()
        )

    if result:
        print(f"Przychód za rok/miesiac {year}/{month} : {result}")



def most_popular_room(session):
    """Zadanie 5c: Pokój z największą liczbą rezerwacji."""
    # TODO: Użyj group_by z func.count
    result = (
        session.query(Room.name, func.count(Reservation.id))
        .join(Room.reservations)
        .group_by(Room.name)
        .order_by(desc(func.count(Reservation.id)))
        .first()
        )

    if result:
        name, total = result
        print(f"Pokój z największą ilością zamówień: {name} | {total}")
    else:
        print("Błąd, nie znaleziono pokoju z największą liczbą rezerwacji")





def top_guest(session):
    """Zadanie 5d: Gosc z najwyzsza kwota."""
    # TODO: Użyj func.sum z order_by

    result = (
        session.query(Guest.name, func.sum(Reservation.total_price))
        .join(Guest.reservations)
        .group_by(Guest.name)
        .order_by(desc(func.sum(Reservation.total_price)))
        .first()
        )

    if result:
        name, total = result
        print(f"Najwyższa kwota należy do: {name} | {total}")





if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            print("\n")            
            clear_all_tables(session)
            seed_data(session)
            print("\n")
            # Różni goście, różne pokoje, różne miesiące

            make_reservation(session, 1, 1, date(2026, 3, 7), date(2026, 3, 14))
            make_reservation(session, 1, 1, date(2026, 3, 1), date(2026, 3, 5))
            make_reservation(session, 2, 2, date(2026, 3, 10), date(2026, 3, 15))
            make_reservation(session, 3, 3, date(2026, 3, 1), date(2026, 3, 8))
            make_reservation(session, 1, 4, date(2026, 4, 1), date(2026, 4, 3))
            make_reservation(session, 4, 1, date(2026, 3, 20), date(2026, 3, 25))

            print("\n")
            check_availability(session, 2, date(2026, 3, 7), date(2026, 3, 21))
            print("\n")
            cancel_reservation(session, 1)
            print("\n")
            active_reservations(session)
            print("\n")
            monthly_revenue(session, 2026, 3)
            print("\n")
            most_popular_room(session)
            print("\n")
            top_guest(session)
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
