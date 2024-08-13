from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import rating_model
# from core.utils import gen_uuid



def rate_movie(db: Session, score: float, movie_id: int, user_id: int):
    db_rating = rating_model.Rating(
        # ruid=gen_uuid(), 
        movie_id=movie_id, 
        score=score,
        user_id=user_id
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating 

def get_rating_by_id(db: Session, rid: int):
    return db.query(rating_model.Rating).filter(rating_model.Rating.id == rid).one_or_none()

def get_movie_ratings(db: Session, movie_id: int):
    avg_ratings_score = db.query(
        func.avg(rating_model.Rating.score).label('avg_rating'),
    ).filter(rating_model.Rating.movie_id == movie_id).scalar()
    total_ratings = db.query(
        func.count(rating_model.Rating.score).label('total_ratings'),
         ).filter(rating_model.Rating.movie_id == movie_id).scalar()
    return {'avg_ratings_score':avg_ratings_score, 'total_ratings':total_ratings}

def get_user_movie_rating(db: Session, movie_id: int, user_id: int):
    return db.query(rating_model.Rating).filter(rating_model.Rating.movie_id == movie_id, rating_model.Rating.user_id == user_id).one_or_none()

