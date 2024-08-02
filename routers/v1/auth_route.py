from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import authenticate_user, create_access_token, pwd_context
from core.database import get_db
from crud import user_crud
from schemas import user_schema
# from app.api.routes import items, login, users, utils

auth_router = APIRouter()

@auth_router.post("/signup", response_model=user_schema.UserResponse)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")
    return user_crud.create_user(db=db, user=user, hashed_password=hashed_password)

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}