from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from logger import logger

from core.security import authenticate_user, create_access_token, pwd_context
from core.database import get_db
from crud import user_crud
from schemas import user_schema
# from app.api.routes import items, login, users, utils

auth_router = APIRouter()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED,  response_model=user_schema.UserResponse)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already registered")
    data = user_crud.create_user(db=db, user=user, hashed_password=hashed_password)
    logger.info(f"User {user.full_name}({user.email}) logged in")
    return {'message': "User Created", 'data': data}

@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: user_schema.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={'user_id': str(user.uuid), 'email': user.email})
    return {"access_token": access_token, "token_type": "bearer"}