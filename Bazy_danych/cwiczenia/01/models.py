from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# TODO: Zdefiniuj model Contact
# Kolumny: id, first_name, last_name, email, phone
# Pamietaj o Primary Key i ograniczeniu UNIQUE na email

class Contact(Base):
    __tablename__ = "contacts"

    # Tutaj zdefiniuj kolumny
    pass
