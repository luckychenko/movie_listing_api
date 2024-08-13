import uuid
from sqlalchemy import UUID, CheckConstraint, Column, DateTime, ForeignKey, Integer, Float, func
from sqlalchemy.orm import relationship

from core.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    ruid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    score = Column(Float, nullable=False) 
    date_created = Column(DateTime, nullable=False, server_default=func.now()) 

    movie = relationship("Movie", back_populates="ratings", lazy='selectin')
    user = relationship("User", back_populates="ratings", lazy='selectin')

    __table_args__ = (
        CheckConstraint('score >= 0 AND score <= 10', name='check_score_range'),
    )
    
    def __repr__(self):
        return f"<Rating(rating={self.score}, movie_id={self.movie_id})>"