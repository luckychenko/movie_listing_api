from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import comment_model
# from core.utils import gen_uuid
from schemas import comment_schema



def post_comment(db: Session, payload: comment_schema.CommentCreate, movie_id: int, user_id: int):
    db_comment = comment_model.Comment(
        # cuid=gen_uuid(), 
        movie_id=movie_id, 
        user_id=user_id,
        content=payload.content,
        parent_id=payload.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment 

def get_comment(db: Session, id: int):
    return db.query(comment_model.Comment).filter(comment_model.Comment.id == id).one_or_none()