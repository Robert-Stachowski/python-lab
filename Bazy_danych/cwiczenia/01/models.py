from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=50), nullable=False )
    last_name = Column(String(length=50), nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)
    phone = Column(String(length=20))

    

