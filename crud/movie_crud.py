from pydantic import UUID4
from sqlalchemy.orm import Session
from models import movie_model
from schemas import movie_schema
from core.utils import gen_uuid

def create_movie(db: Session, movie: movie_schema.MovieCreate, user_id: int):
    db_movie = movie_model.Movie(
        muid=gen_uuid(), 
        title=movie.title, 
        description=movie.description,
        user_id=user_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_movie_by_title(db: Session, title: str):
    return db.query(movie_model.Movie).filter(movie_model.Movie.title == title).one_or_none()

def get_movie(db: Session, muid: UUID4):
    return db.query(movie_model.Movie).filter(movie_model.Movie.muid == muid).one_or_none()

def get_movies(db: Session, offset: int = 0, limit: int = 10):
    return db.query(movie_model.Movie).offset(offset).limit(limit).all()
    
def update_movie(db: Session, movie: movie_model.Movie, movie_payload: movie_schema.MovieUpdate):
    #update only values user set, ignore unset
    movie_payload_dict = movie_payload.model_dump(exclude_unset=True)
    for k, v in movie_payload_dict.items():
        setattr(movie, k, v)
    # update DB
    db.add(movie)
    db.commit()
    db.refresh(movie)

    return movie

def delete_movie(db: Session, movie: movie_model.Movie,):
    db.delete(movie)
    db.commit()
    return True
