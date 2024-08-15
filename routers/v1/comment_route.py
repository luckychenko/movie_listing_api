
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
from core.utils import to_pydantic

comment_router = APIRouter()


@comment_router.post("/", status_code=status.HTTP_201_CREATED,  response_model=comment_schema.CommentResponse)
def add_comment(payload: comment_schema.CommentCreate,  user: user_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # confirm movie is in DB
    movie = movie_crud.get_movie(db, payload.movie_id)
    if not movie:  
        # log activity
        logger.error(f"{user.email} trying to comment on non existing movie ({payload.movie_id})")      
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie you are trying to comment on does not exists")
    
    # supports nested commenting (reply to a comment)
    db_comment = comment_crud.post_comment(db, payload, movie.id, user.id)
    # log activity
    logger.info(f"User {user.full_name}({user.email}) Commented on ({movie.title})")
    return {'message': "Comment Added", 'data': db_comment}


@comment_router.get("/{movie_id}", status_code=status.HTTP_200_OK,  response_model=comment_schema.CommentResponse)
def get_comments(movie_id: UUID4, offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # confirm movie is in DB
    movie = movie_crud.get_movie(db, movie_id)
    if not movie:   
        # log activity
        logger.error(f"user trying to view comment on non existing movie ({movie_id})")        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    res = comment_crud.get_movie_comments(db, movie.id, offset, limit)
    # Convert result to a list of dictionaries
    data = [comment_schema.CommentOut.model_validate(comment) for comment in res]    
    return {'message': "Success", 'data': data}
    