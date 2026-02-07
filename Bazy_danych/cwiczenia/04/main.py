from models import Base, Category, Product
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)


def seed_data(session):
    """Zadanie 1: Dodaj kategorie i produkty."""
    # TODO: Utworz kategorie i produkty
    pass


def total_products(session):
    """Zadanie 2a: Laczna liczba produktow."""
    # TODO: Uzyj func.count()
    pass


def avg_price(session):
    """Zadanie 2b: Srednia cena."""
    # TODO: Uzyj func.avg()
    pass


def min_max_price(session):
    """Zadanie 2c: Najtanszy i najdrozszy produkt."""
    # TODO: Uzyj func.min() i func.max()
    pass


def total_inventory_value(session):
    """Zadanie 2d: Laczna wartosc magazynu."""
    # TODO: Uzyj func.sum(Product.price * Product.quantity)
    pass


def products_per_category(session):
    """Zadanie 3a: Liczba produktow na kategorie."""
    # TODO: Uzyj group_by z func.count()
    pass


def avg_price_per_category(session):
    """Zadanie 3b: Srednia cena na kategorie."""
    # TODO: Uzyj group_by z func.avg()
    pass


def categories_value_over_1000(session):
    """Zadanie 3c: Kategorie z wartoscia > 1000 zl."""
    # TODO: Uzyj having()
    pass


def top_5_expensive(session):
    """Zadanie 4a: 5 najdrozszych produktow."""
    # TODO: Uzyj order_by(desc) z limit(5)
    pass


def low_stock(session):
    """Zadanie 4b: Produkty z iloscia < 5."""
    # TODO: Uzyj filter
    pass


def categories_sorted_by_count(session):
    """Zadanie 4c: Kategorie posortowane po liczbie produktow."""
    # TODO: Uzyj group_by, func.count, order_by
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
