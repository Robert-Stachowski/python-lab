from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserResponse



router = APIRouter(prefix="/auth", tags=["auth"])






@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nazwa użytkownika jest już zajęta")
    
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email jest już używany")
    
    
    hashed = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user








@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nieprawidłowy email lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}