from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import comment_model
# from core.utils import gen_uuid
from schemas import comment_schema



def post_comment(db: Session, payload: comment_schema.CommentCreate, movie_id: int, user_id: int):
    db_comment = comment_model.Comment(
        movie_id=movie_id, 
        user_id=user_id,
        content=payload.content,
        parent_id=payload.parent_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment 

def get_movie_comments(db: Session, movie_id: int, offset: int = 0, limit: int = 10):
    # added "comment_model.Comment.parent_id == None" filter to remove duplicate cascades
    # to allow the replies relationship take care of the nested comments (it creates a tree-like response)
    return db.query(comment_model.Comment).filter(comment_model.Comment.movie_id == movie_id, comment_model.Comment.parent_id == None).offset(offset).limit(limit).all()

def get_comment(db: Session, id: int):
    return db.query(comment_model.Comment).filter(comment_model.Comment.id == id).one_or_none()