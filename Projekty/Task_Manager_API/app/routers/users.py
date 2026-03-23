from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

# TODO: Zaimportuj modele, schematy i get_db
from ..database import get_db
from ..import models
from ..schemas.user import UserUpdate, UserResponse
from ..schemas.pagination import PaginatedResponse

from app.auth.dependencies import get_current_user
from app.models import User




router = APIRouter()


# Endpoint dostępny tylko dla zalogowanych
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user







@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    skip: int = Query(default=0, ge=0),          # ge=0: skip >= 0
    limit: int = Query(default=10, ge=1, le=100), # limit: od 1 do 100
    db: Session = Depends(get_db)
    ):

    """Pobierz liste uzytkownikow.""" 
    # + paginacja

    total = db.query(models.User).count() # wracam liczbę wszytskich rekordów
    items = db.query(models.User).offset(skip).limit(limit).all() # zwracam rekordy od 0 - 10.

    return PaginatedResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=items
    )
    


    




@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Pobierz uzytkownika po ID."""
    # Jesli nie znaleziono -> HTTPException(404)
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")
    return db_user
    




@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Zaktualizuj uzytkownika."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user




@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Usun uzytkownika."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="NIe znaleziono usera")
    db.delete(db_user)
    db.commit()
