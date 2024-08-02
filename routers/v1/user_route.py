from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from crud import user_crud
from schemas import user_schema
# from app.api.routes import items, login, users, utils

user_router = APIRouter()

@user_router.delete("/delete", response_model=user_schema.UserResponse)
def delete_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already registered")
    return user_crud.create_user(db=db, user=user, hashed_password=hashed_password)

