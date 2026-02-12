from models import Base, Category, Product
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc



def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)



def clear_tables(session):
    create_tables()
    session.query(Product).delete()
    session.query(Category).delete()
    session.commit()



def seed_data(session):
    """Zadanie 1: Dodaj kategorie i produkty."""

    categories = [
        Category(name="sprzątające", category_rel = [
            Product(name="Odkurzacz", price=300.0, quantity=5),
            Product(name="Mop parowy", price=180.0, quantity=7),
            Product(name="Ściereczki z mikrofibry", price=25.0, quantity=30),
        ]),
        Category(name="prasujące", category_rel = [
            Product(name="Żelazko", price=150.0, quantity=4),
            Product(name="Deska do prasowania", price=220.0, quantity=3),
        ]),
        Category(name="kuchenne", category_rel = [
            Product(name="Czajnik elektryczny", price=120.0, quantity=6),
            Product(name="Toster", price=90.0, quantity=8),
            Product(name="Blender", price=200.0, quantity=5),
        ]),
        Category(name="elektronika", category_rel = [
            Product(name="Smartfon", price=2500.0, quantity=2),
            Product(name="Słuchawki bezprzewodowe", price=400.0, quantity=10),
        ])
    ]

    
    
    session.add_all(categories)
    session.commit()


def total_products(session):
    """Zadanie 2a: Łączna liczba produktów."""
    
    count = session.query(func.count(Product.id)).scalar()
    print(f"Łączna ilość produktów {count}")
    
    sum_qty = session.query(func.sum(Product.quantity)).scalar()
    print(f"Łączna ilość sztuk: {sum_qty or 0}")



def avg_price(session):
    """Zadanie 2b: Średnia cena."""
    # TODO: Użyj func.avg()
    result = session.query(func.avg(Product.price)).scalar()
    print(f"Średnia cena produktów: {(result or 0):.2f} ")



def min_max_price(session):
    """Zadanie 2c: Najtanszy i najdroższy produkt."""
    # TODO: Użyj func.min() i func.max()
    max_min_result = (session.query(
        func.max(Product.price).label("max_r"), 
        func.min(Product.price).label("min_r")).
        one())
    
    print(f"MAX: {(max_min_result.max_r or 0):.2f}, MIN: {(max_min_result.min_r or 0):.2f}")
    

def total_inventory_value(session):
    """Zadanie 2d: Łączna wartość magazynu."""
    # TODO: Użyj func.sum(Product.price * Product.quantity)
    result = session.query(func.sum(Product.price*Product.quantity)).scalar()
    print(f"Łączna wartość magazynu: {result or 0} ")


def products_per_category(session):
    """Zadanie 3a: Liczba produktów na kategorie."""
    # TODO: Użyj group_by z func.count()
    result = session.query(Category.name, func.count(Product.id)).join(Product).group_by(Category.name).all()
    for name, count in result:
        print(f" Kategoria: {name} Liczba produktów na kategorię: {count} ")



def avg_price_per_category(session):
    """Zadanie 3b: Srednia cena na kategorie."""
    # TODO: Użyj group_by z func.avg()
    result = session.query(Category.name, func.avg(Product.price)).join(Product).group_by(Category.name).all()
    for name, avg_p in result:
        print(f"Kategoria: {name} średnia cena: {avg_p:.2f}")




def categories_value_over_1000(session):
    """Zadanie 3c: Kategorie z wartością > 1000 zl."""
    # TODO: Użyj having()
    result = (session.query(Category.name, func.sum(Product.price*Product.quantity).label("sum_p"))
              .join(Product)
              .group_by(Category.name)
              .having(func.sum(Product.price*Product.quantity) > 1000)
              .all())
    for name, sum_p in result:
        print(f"Kategorie z wartością powyżej 1000 złotych: Kategoria: {name}, Wartość: {sum_p} ")


def top_5_expensive(session):
    """Zadanie 4a: 5 najdroższych produktów."""
    # TODO: Użyj order_by(desc) z limit(5)
    result = session.query(Product).order_by(desc(Product.price)).limit(5).all()
    for product in result:
        print(f"Najdroższe produkty - Produkty: {product.name} cena: {product.price:.2f}")


def low_stock(session):
    """Zadanie 4b: Produkty z iloscia < 5."""
    # TODO: Użyj filter
    result = session.query(Product).filter(Product.quantity < 5).all()
    for product in result:
        print(f"Produkty poniżej pięciu sztuk:  Produkt: {product.name} Sztuk: {product.quantity} ")


def categories_sorted_by_count(session):
    """Zadanie 4c: Kategorie posortowane po liczbie produktow."""
    # TODO: Użyj group_by, func.count, order_by
    result = ( session.query(Category.name, func.count(Product.id).label("count_p"))
        .join(Product)
        .group_by(Category.name)
        .order_by(desc(func.count(Product.id)))
        .all()
    )
    for category, count_p in result:
        print(f"Kategoria: {category} Ilość produktów: {count_p}")


if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            clear_tables(session)
            seed_data(session)
            print("\n")
            total_products(session)
            print("\n")
            avg_price(session)
            print("\n")
            min_max_price(session)
            print("\n")
            total_inventory_value(session)
            print("\n")
            products_per_category(session)
            print("\n")
            avg_price_per_category(session)
            print("\n")
            categories_value_over_1000(session)
            print("\n")
            top_5_expensive(session)
            print("\n")
            low_stock(session)
            print("\n")
            categories_sorted_by_count(session)



        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
