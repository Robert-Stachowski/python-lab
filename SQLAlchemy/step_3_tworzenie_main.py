from step_2_tworzenie_tabeli import User, Base
from step_1_tworzenie_sesji import Session, engine

Base.metadata.create_all(engine)
session = Session()


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
session.commit()
session.close()