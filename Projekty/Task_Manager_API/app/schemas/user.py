from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# TODO: Zdefiniuj schematy Pydantic dla User

# Schema do tworzenia uzytkownika (request body dla POST)
# class UserCreate(BaseModel):
#     username: str
#     email: str
#     pass

# Schema do aktualizacji (request body dla PUT)
# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     email: Optional[str] = None
#     is_active: Optional[bool] = None

# Schema odpowiedzi (response body)
# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: str
#     is_active: bool
#     created_at: datetime
#
#     class Config:
#         from_attributes = True  # Pozwala na konwersje z obiektow SQLAlchemy
