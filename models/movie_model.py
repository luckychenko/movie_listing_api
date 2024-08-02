
from sqlalchemy import UUID, Column, String, Integer, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
import uuid

from core.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True, nullable=False)
    title = Column(String(255), unique=True, index=True)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="movies", lazy='selectin') 
    ratings = relationship("Rating", back_populates="movie", lazy='selectin')
    comments = relationship("Comment", back_populates="movie", lazy='selectin')


    def __repr__(self):
        return f"<Movie(title={self.title}, uuid={self.uuid})>"