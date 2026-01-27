from step_1_tworzenie_sesji import engine, Session
from step_2_tworzenie_tabeli import Base, User

# tworzenie tabel (tylko do nauki / SQLite)
Base.metadata.create_all(engine)

try:
    # Session.begin():
    # - otwiera sesję
    # - rozpoczyna transakcję
    # - commit przy sukcesie
    # - rollback przy wyjątku
    # - zamyka sesję automatycznie
    
    with Session.begin() as session:
        user = User(
            username="admin",
            password="Please don't set passwords like this",
            email="admin@example.com",
            first_name="Todd",
            last_name="Birchard",
            bio="I write tutorials on the internet.",
            avatar_url="https://example.com/avatar.jpg"
        )

        session.add(user)

except Exception as exc:
    # rollback już się wydarzył w Session.begin()
    print(f"Błąd zapisu do bazy: {exc}")
