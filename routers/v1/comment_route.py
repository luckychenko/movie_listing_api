
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.orm import Session

from logger import logger
from core.database import get_db
from crud import comment_crud, movie_crud
from schemas import comment_schema, user_schema
from core.security import get_current_user

comment_router = APIRouter()


@comment_router.post("/", status_code=status.HTTP_201_CREATED,  response_model=comment_schema.CommentResponse)
def add_comment(payload: comment_schema.CommentCreate,  user: user_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # confirm movie is in DB
    movie = movie_crud.get_movie(db, payload.movie_id)
    if not movie:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie you are trying to comment on does not exist")
    
    db_comment = comment_crud.post_comment(db, payload, movie.id, user.id)
    # log activity
    logger.info(f"User {user.full_name}({user.email}) Commented on ({movie.title})")
    return {'message': "Success", 'data': db_comment}