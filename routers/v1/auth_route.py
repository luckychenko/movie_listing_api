
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from logger import logger

from core.security import authenticate_user, create_access_token, pwd_context
from core.database import get_db
from crud import user_crud
from schemas import user_schema

auth_router = APIRouter()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED,  response_model=user_schema.UserResponse)
def signup(payload: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=payload.email)
    hashed_password = pwd_context.hash(payload.password)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already registered")
    # create user record
    res = user_crud.create_user(db=db, user=payload, hashed_password=hashed_password)
    # log activity
    logger.info(f"User {payload.full_name}({payload.email}) Signed Up")
    return {'message': "User Created", 'data': res}

@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: user_schema.UserLogin = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # create auth token
    access_token = create_access_token(data={'email': str(user.email)}) 
    # log activity   
    logger.info(f"User {user.full_name}({user.email}) Logged In")
    return {"access_token": access_token, "token_type": "bearer"}