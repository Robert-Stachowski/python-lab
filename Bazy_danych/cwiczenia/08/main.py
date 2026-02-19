import sys
sys.stdout.reconfigure(encoding='utf-8')

from models import Base, Customer, Product, Order
from db import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from datetime import datetime, timedelta


def create_tables():
    """Tworzy tabele w bazie danych."""
    Base.metadata.create_all(engine)

def clear_all_tables(session):
    create_tables()
    session.query(Order).delete()
    session.query(Product).delete()
    session.query(Customer).delete()
    session.commit()


def seed_data(session):
    """Zadanie 1: Dodaj klientów, produkty i zamówienia."""
    # TODO: Seedowanie danych

    laptop = Product(name='Laptop 14" Pro', price=4299.00, category="Elektronika")
    phone = Product(name="Smartfon X", price=2999.00, category="Elektronika")
    headphones = Product(name="Słuchawki ANC", price=599.00, category="Elektronika")
    monitor = Product(name='Monitor 27" 144Hz', price=1299.00, category="Elektronika")

    coffee = Product(name="Kawa ziarnista 1kg", price=79.90, category="Spożywcze")
    olive_oil = Product(name="Oliwa extra virgin 1L", price=39.90, category="Spożywcze")
    pasta = Product(name="Makaron premium 500g", price=12.50, category="Spożywcze")

    detergent = Product(name="Płyn do naczyń 1L", price=11.99, category="Dom")
    towels = Product(name="Papier ręcznikowy 6 rolek", price=19.99, category="Dom")
    powder = Product(name="Proszek do prania 4kg", price=54.99, category="Dom")

    unused = Product(name="Tablet 10 cali", price=1599.00, category="Elektronika")

    session.add_all([
        laptop, phone, headphones, monitor,
        coffee, olive_oil, pasta,
        detergent, towels, powder, unused
    ])
    
    now = datetime.utcnow()
    customers = [
        Customer(
            name="Robert Nowak",
            email="robert.nowak@example.com",
            city="Poznań",
            orders=[
                Order(product=laptop, quantity=1, order_date=now -timedelta(days=6)),
                Order(product=headphones, quantity=2, order_date=now -timedelta(days=1)),
                Order(product=coffee, quantity=3, order_date=now -timedelta(days=4)),
                Order(product=towels, quantity=2, order_date=now -timedelta(days=8)),
            ],
        ),
        Customer(
            name="Anna Kowalska",
            email="anna.kowalska@example.com",
            city="Warszawa",
            orders=[
                Order(product=phone, quantity=1, order_date=now -timedelta(days=17)),
                Order(product=monitor, quantity=1, order_date=now -timedelta(days=4)),
                Order(product=olive_oil, quantity=4, order_date=now),
                Order(product=detergent, quantity=3, order_date=now -timedelta(days=11)),
            ],
        ),
        Customer(
            name="Piotr Zieliński",
            email="piotr.zielinski@example.com",
            city="Kraków",
            orders=[
                Order(product=headphones, quantity=1, order_date=now -timedelta(days=11)),
                Order(product=pasta, quantity=6, order_date=now -timedelta(days=2)),
                Order(product=coffee, quantity=1, order_date=now -timedelta(days=9)),
            ],
        ),
        Customer(
        name="Michał Kaczmarek",
        email="michal.kaczmarek@example.com",
        city="Łódź",
        orders=[
            Order(product=phone, quantity=1, order_date=now - timedelta(days=1)),
            Order(product=coffee, quantity=2, order_date=now - timedelta(days=2)),
            Order(product=detergent, quantity=4, order_date=now - timedelta(days=6)),
        ],
        ),
        Customer(
            name="Agnieszka Dąbrowska",
            email="agnieszka.dabrowska@example.com",
            city="Katowice",
            orders=[
                Order(product=laptop, quantity=1, order_date=now - timedelta(days=11)),
                Order(product=olive_oil, quantity=3, order_date=now - timedelta(days=8)),
                Order(product=towels, quantity=2, order_date=now - timedelta(days=1)),
                Order(product=powder, quantity=1, order_date=now - timedelta(days=5)),
            ],
        ),
    ]

    session.add_all(customers)
    session.commit()
    print(" Seedowanie zakończone")



def total_sales(session):
    """Zadanie 2a: Łączna wartość zamówień."""
    # TODO: Użyj func.sum(Product.price * Order.quantity)
    result = session.query(func.sum(Product.price * Order.quantity)).join(Order.product).scalar()
    if result:
        print(f"--- Wartość zamówień łącznie: {result} ---")


def avg_order_value(session):
    """Zadanie 2b: Średnia wartość zamówienia."""
    # TODO: Użyj func.avg
    
    result = session.query(func.avg(Product.price * Order.quantity)).join(Order.product).scalar()
    if result:
        print(f"--- Średnia wartość zamówienia: {result} ---")

def orders_per_customer(session):
    """Zadanie 2c: Liczba zamówień na klienta."""
    # TODO: Użyj group_by z func.count
    
    result = (
        session.query(Customer.name, func.count(Order.id))
        .join(Order.customer)
        .group_by(Customer.name)
        .order_by(desc(func.count(Order.id)))
        .all()
        )
    
    for name, count in result:
        print(f"--- Klient: {name}, ilość zamówień: {count}")


def customers_above_average(session):
    """Zadanie 3a: Klienci powyżej średniej.(suma wartosci koszyka klienta do średniej wartości zamówień wszystkich klientów)"""
    # TODO: Użyj scalar_subquery()
    
    #Łączna wartość zamówienia dla każdego klienta:
    customer_totals = (
        session.query(func.sum(Product.price * Order.quantity).label("total"))
        .join(Order.product)
        .group_by(Order.customer_id)
        .subquery()
        )
    
    #Policz średnią zamówienia dla każdego klienta
    avg_spending = session.query(func.avg(customer_totals.c.total)).scalar_subquery()

    #Klienci powyżej średniej:
    result = (
        session.query(Customer.name, func.sum(Product.price * Order.quantity))
        .join(Customer.orders)
        .join(Order.product)
        .group_by(Customer.name)
        .having(func.sum(Product.price * Order.quantity) > avg_spending)
        .all())
    
    for name, avg in result:
        print(f"--- Klienci powyżej średniej: {name} : ({avg:.2f})")




def customers_above_average_avg(session):
    """Zadanie 3a: Klienci powyżej średniej.(ŚREDNIA wartosci koszyka klienta do średniej wartości zamówień wszystkich klientów)"""
    # TODO: Użyj scalar_subquery()
    
    #Łączna wartość zamówienia dla każdego klienta:
    customer_totals = (
        session.query(func.avg(Product.price * Order.quantity).label("total"))
        .join(Order.product)
        .group_by(Order.customer_id)
        .subquery()
        )
    
    #Policz średnią zamówienia dla każdego klienta
    avg_spending = session.query(func.avg(customer_totals.c.total)).scalar_subquery()

    #Klienci powyżej średniej:
    result = (
        session.query(Customer.name, func.avg(Product.price * Order.quantity))
        .join(Customer.orders)
        .join(Order.product)
        .group_by(Customer.name)
        .having(func.avg(Product.price * Order.quantity) > avg_spending)
        .all())
    
    for name, avg in result:
        print(f"--- Klienci powyżej średniej: {name} : ({avg:.2f})")



def products_never_ordered(session):
    """Zadanie 3b: Produkty nigdy nie zamówione."""
    # TODO: Użyj NOT IN z subquery
    ordered_ids = session.query(Order.product_id).scalar_subquery()
    result = session.query(Product).filter(~Product.id.in_(ordered_ids)).all()
    if result:        
        print("--- Produkty nigdy nie zamówione:  ---")
        for product in result:
            print(f" {product.name} : {product.price} zł")
    else:
        print("Brak produktów nigdy nie zamawianych")


def top_customer(session):
    """Zadanie 3c: Klient z najwyższą kwotą."""
    # TODO: Użyj subquery + order_by
    customer_total = (
        session.query(Order.customer_id, func.sum(Product.price * Order.quantity).label("total"))
        .join(Order.product)
        .group_by(Order.customer_id)
        .subquery()
        )
    
    result = (
        session.query(Customer.name, customer_total.c.total)
        .join(customer_total, Customer.id == customer_total.c.customer_id)
        .order_by(desc(customer_total.c.total))
        .limit(1)
        .first()
        )
    if result:
        name, total = result
        print(f" Największa wartość: {name} : {total} zł")

    # Prostsze, bez subquery - jedno zapytanie:
    result_2 = (
        session.query(Customer.name, func.sum(Product.price * Order.quantity))
        .join(Customer.orders)
        .join(Order.product)        
        .group_by(Customer.name)
        .order_by(desc(func.sum(Product.price * Order.quantity)))
        .limit(1)
        .first()
        )
    if result_2:
        name, total = result_2
        print(f"--- Top klient: {name} ({total:.2f} zł) ---")




def categories_over_500(session):
    """Zadanie 4a: Kategorie z łączną sprzedażą > 500."""
    # TODO: Użyj having()
    result = (
        session.query(Product.category, func.sum(Product.price * Order.quantity))
        .join(Order.product)
        .group_by(Product.category)
        .having(func.sum(Product.price * Order.quantity) > 500)
        .all()
        )
    print(f"--- Kategorie z większą sprzedażą niż 500zł: ---")
    for category, total in result:
        print(f" {category} : {total} ")



def cities_over_3_orders(session):
    """Zadanie 4b: Miasta z > 3 zamowieniami."""
    # TODO: Użyj having()
    result = (session.query(Customer.city, func.count(Order.id))
             .join(Order.customer)
             .group_by(Customer.city)
             .having(func.count(Order.id) > 3)             
             .all()
             )
    for city, total in result:
        print(f"--- {city}, ilość zamówień: {total} ---")


def monthly_sales(session):
    """Zadanie 4c: Sprzedaż miesieczna."""
    # TODO: Użyj func.extract('month', Order.order_date)
    result = (
        session.query(
            func.extract('month', Order.order_date), 
            func.sum(Product.price * Order.quantity),
            func.count(Order.id)
            )
        .join(Order.product)
        .group_by(func.extract('month', Order.order_date))
        .order_by(func.extract('month', Order.order_date))
        .all())
    print("--- Sprzedaż miesieczna: ---")
    for month, total, count in result:
        print(f"Miesiąc {month}: {total:.2f} zł ({count} zamówień)")



def top_3_products(session):
    """Zadanie 5a: Top 3 produkty."""
    # TODO: Użyj func.count z order_by(desc) i limit(3)
    result = (
        session.query(Product.name, func.count(Order.id))
        .join(Order.product)
        .group_by(Product.name)
        .order_by(desc(func.count(Order.id)))
        .limit(3)
        .all()
        )
    for name, count in result:
        print(f"--- Top produkt: {name}, ilość: {count} ---")


def top_3_customers(session):
    """Zadanie 5b: Top 3 klienci."""
    # TODO: Użyj func.sum z order_by(desc) i limit(3)
    result = (
        session.query(Customer.name, func.sum(Product.price * Order.quantity))
        .join(Customer.orders)
        .join(Order.product)
        .group_by(Customer.name)
        .order_by(desc(func.sum(Product.price * Order.quantity)))
        .limit(3)
        .all()
        )
    for name, total in result:
        print(f"--- Top klienci: {name} : {total} zł")


def category_report(session):
    """Zadanie 5c: Raport po kategoriach."""
    # TODO: Grupuj po kategorii, oblicz count, sum, avg
    result = (
        session.query(
            Product.category, 
            func.count(Order.id), 
            func.sum(Product.price * Order.quantity), 
            func.avg(Product.price * Order.quantity)
            )
            .join(Order.product)
            .group_by(Product.category)
            .order_by(desc(func.count(Order.id)))
            .all()
    )
    print(f"--- Raport po kategoriach ---")
    for name, count, total, avg_t in result:
        print(f" Kategoria: {name}, ilość {count}, suma: {total}, średnia: {avg_t}")



if __name__ == "__main__":
    create_tables()

    with SessionLocal() as session:
        try:
            
            clear_all_tables(session)
            print("\n")
            seed_data(session)
            print("\n")
            total_sales(session)
            print("\n")
            avg_order_value(session)
            print("\n")
            orders_per_customer(session)
            print("\n")
            customers_above_average(session)
            print("\n")
            customers_above_average_avg(session)
            print("\n")
            products_never_ordered(session)
            print("\n")
            top_customer(session)
            print("\n")
            categories_over_500(session)
            print("\n")
            cities_over_3_orders(session)
            print("\n")
            monthly_sales(session)
            print("\n")
            top_3_products(session)
            print("\n")
            top_3_customers(session)
            print("\n")
            category_report(session)
            
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Błąd bazy danych: {e}")
