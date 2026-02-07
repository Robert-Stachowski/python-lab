from models import Base, Customer, Product, Order
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime, timedelta


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Zadanie 1: Dodaj klientow, produkty i zamowienia."""
    # TODO: Seedowanie danych
    pass


def total_sales(session):
    """Zadanie 2a: Laczna wartosc zamowien."""
    # TODO: Uzyj func.sum(Product.price * Order.quantity)
    pass


def avg_order_value(session):
    """Zadanie 2b: Srednia wartosc zamowienia."""
    # TODO: Uzyj func.avg
    pass


def orders_per_customer(session):
    """Zadanie 2c: Liczba zamowien na klienta."""
    # TODO: Uzyj group_by z func.count
    pass


def customers_above_average(session):
    """Zadanie 3a: Klienci powyzej sredniej."""
    # TODO: Uzyj scalar_subquery()
    pass


def products_never_ordered(session):
    """Zadanie 3b: Produkty nigdy nie zamowione."""
    # TODO: Uzyj NOT IN z subquery
    pass


def top_customer(session):
    """Zadanie 3c: Klient z najwyzsza kwota."""
    # TODO: Uzyj subquery + order_by
    pass


def categories_over_500(session):
    """Zadanie 4a: Kategorie z laczna sprzedaza > 500."""
    # TODO: Uzyj having()
    pass


def cities_over_3_orders(session):
    """Zadanie 4b: Miasta z > 3 zamowieniami."""
    # TODO: Uzyj having()
    pass


def monthly_sales(session):
    """Zadanie 4c: Sprzedaz miesieczna."""
    # TODO: Uzyj func.extract('month', Order.order_date)
    pass


def top_3_products(session):
    """Zadanie 5a: Top 3 produkty."""
    # TODO: Uzyj func.count z order_by(desc) i limit(3)
    pass


def top_3_customers(session):
    """Zadanie 5b: Top 3 klienci."""
    # TODO: Uzyj func.sum z order_by(desc) i limit(3)
    pass


def category_report(session):
    """Zadanie 5c: Raport po kategoriach."""
    # TODO: Grupuj po kategorii, oblicz count, sum, avg
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
