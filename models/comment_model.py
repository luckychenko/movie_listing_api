from sqlalchemy import UUID, Column, Index, String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from core.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    comment = Column(String, nullable=False)    
    parent = Column(Integer, nullable=True, index=True)  
    date_created = Column(DateTime, nullable=False, server_default=func.now())  
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())

    movie = relationship("Movie", back_populates="comments", lazy='selectin') 
    user = relationship("User", back_populates="comments", lazy='selectin') 

    __table_args__ = (
        Index('ix_comments_movie_user', 'movie_id', 'user_id'),
    )

    def __repr__(self):
        return f"<Comment(comment={self.comment}, movie_id={self.movie_id})>"