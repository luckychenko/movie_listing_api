from sqlalchemy.orm import Session
from models import user_model
from schemas import user_schema
from core.utils import gen_uuid

def create_user(db: Session, user: user_schema.User, hashed_password: str) -> user_schema.UserOut:
    db_user = user_model.User(
        uuid=gen_uuid(), 
        email=user.email, 
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user_schema.UserOut(user_id=db_user.uuid, email=db_user.email, full_name=db_user.full_name)

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()