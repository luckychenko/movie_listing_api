
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.orm import Session

from logger import logger
from core.database import get_db
from crud import movie_crud, rating_crud
from schemas import rating_schema, user_schema
from core.security import get_current_user

rating_router = APIRouter()



@rating_router.post("/", status_code=status.HTTP_201_CREATED, response_model=rating_schema.RatingResponse)
def rate_movie(payload: rating_schema.RatingCreate,  user: user_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):    
    # confirm movie is in DB
    movie = movie_crud.get_movie(db, payload.movie_id)
    if not movie:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie you are trying to rate does not exist")
    
    # verify if user had already rated same movie
    rated = rating_crud.get_user_movie_rating(db, movie.id, user.id)
    if rated:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You already rated this movie")
    
    res = rating_crud.rate_movie(db, payload.score, movie.id, user.id)
    #format output data
    data = rating_schema.RatingOut(id=res.id, movie_id=movie.muid, score=res.score, user=res.user)
    # log activity
    logger.info(f"User {user.full_name}({user.email}) Rated movie ({movie.title})")
    return {'message': "Movie Rated", 'data': data}
    

@rating_router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=rating_schema.RatingResponse)
def get_ratings(movie_id: UUID4, db: Session = Depends(get_db)):
    # confirm movie is in DB
    movie = movie_crud.get_movie(db, movie_id)
    if not movie:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie you are trying to rate does not exist")
    
    res = rating_crud.get_movie_ratings(db, movie.id)
    data = rating_schema.RatingScoreOut(movie_id=movie.muid, avg_ratings_score=res['avg_ratings_score'], total_ratings=res['total_ratings'])
    
    return {'message': "Success", 'data': data}
    





