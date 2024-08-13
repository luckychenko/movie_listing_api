from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from logger import logger
from core.database import get_db
from crud import movie_crud
from schemas import movie_schema, user_schema
from core.security import get_current_user

movie_router = APIRouter()


@movie_router.post("/", status_code=status.HTTP_201_CREATED,  response_model=movie_schema.MovieResponse)
def add_movie(payload: movie_schema.MovieCreate,  user: user_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_movie = movie_crud.get_movie_by_title(db, payload.title)
    if db_movie:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Movie with title '{payload.title}' already exists")
    res = movie_crud.create_movie(db, payload, user.id)
    # log activity
    logger.info(f"User {user.full_name}({user.email}) Added Movie ({res.title})")
    return {'message': "Movie Added", 'data': res}
    


@movie_router.get("/", status_code=status.HTTP_200_OK, response_model=movie_schema.MovieResponse)
def get_movies(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_movies = movie_crud.get_movies(db=db, offset = offset, limit = limit)
    if not db_movies:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="No movies in database"
                             )
    return {'message': "Success", 'data': db_movies}


@movie_router.get("/{movie_id}", status_code=status.HTTP_200_OK, response_model=movie_schema.MovieResponse)
def get_movie(movie_id: UUID4, db: Session = Depends(get_db)):
    db_movie = movie_crud.get_movie(db=db, muid=movie_id)
    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found" )
    return {'message': "Success", 'data': db_movie}


@movie_router.put('/{movie_id}', status_code=status.HTTP_200_OK, response_model=movie_schema.MovieResponse)
def update_update(movie_id: UUID4, payload: movie_schema.MovieUpdate, user: user_schema.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # confirm movie is in DB
    movie = movie_crud.get_movie(db, movie_id)
    if not movie:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if movie.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action forbidden, You are not authorized to modify this movie")
    
    db_movie = movie_crud.update_movie(db, movie, payload)
    # log activity
    logger.info(f"User {user.full_name}({user.email}) Updated Movie ({movie.title})")
    return {'message': 'Movie Updated', 'data': db_movie}


@movie_router.delete("/{movie_id}", status_code=status.HTTP_200_OK, response_model=movie_schema.MovieResponse)
def delete_movie(movie_id: UUID4, db: Session = Depends(get_db), user: user_schema.User = Depends(get_current_user)):
    # confirm movie is in DB
    movie = movie_crud.get_movie(db, movie_id)
    if not movie:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    if movie.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action forbidden, You are not authorized to delete this movie")
    
    movie_crud.delete_movie(db, movie)
    # log activity
    logger.info(f"User {user.full_name}({user.email}) Deleted Movie ({movie.title})")
    return {'message': 'Movie Deleted'}

