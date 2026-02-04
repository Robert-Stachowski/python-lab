from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    # user account
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(Text)
    avatar_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now()) #server_default ustawia wartość(czas) po stronie bazy danych przy INSERT, 
    updated_at = Column(DateTime, server_default=func.now()) # więc po commit() w ORM może być None i trzeba zrobić session.refresh(obj).

    def __repr__(self):
        return f"User: {self.username}" # __repr__ definiuje czytelną reprezentację obiektu w Pythonie (print, logi, debug),
                                        # nie ma wpływu na bazę danych ani na ORM.

