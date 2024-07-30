from sqlalchemy.orm import Session
from models import user_model
from schemas import user_schema

def create_user(db: Session, user: user_schema.UserCreate, hashed_password: str):
    db_user = user_model.User(
        email=user.email, 
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()