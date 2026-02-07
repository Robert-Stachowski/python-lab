from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# TODO: Zaimportuj modele, schematy i get_db
# from ..database import get_db
# from .. import models
# from ..schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()


# TODO: Zaimplementuj endpointy CRUD dla User

# @router.get("/", response_model=list[UserResponse])
# def get_users(db: Session = Depends(get_db)):
#     """Pobierz liste uzytkownikow."""
#     pass

# @router.post("/", response_model=UserResponse, status_code=201)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     """Utworz nowego uzytkownika."""
#     # Sprawdz czy username/email juz istnieje
#     # Utworz i zapisz uzytkownika
#     pass

# @router.get("/{user_id}", response_model=UserResponse)
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     """Pobierz uzytkownika po ID."""
#     # Jesli nie znaleziono -> HTTPException(404)
#     pass

# @router.put("/{user_id}", response_model=UserResponse)
# def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
#     """Zaktualizuj uzytkownika."""
#     pass

# @router.delete("/{user_id}", status_code=204)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     """Usun uzytkownika."""
#     pass
