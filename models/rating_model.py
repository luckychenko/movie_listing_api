from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from core.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    rating = Column(Float, nullable=False)

    movie = relationship("Movie", back_populates="ratings", lazy='selectin')
    user = relationship("User", back_populates="ratings", lazy='selectin')


    def __repr__(self):
        return f"<Rating(rating={self.rating}, movie_id={self.movie_id})>"