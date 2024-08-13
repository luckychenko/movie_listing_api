from sqlalchemy import UUID, Column, Index, String, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship
import uuid 

from core.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    # cuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True, nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    content = Column(String, nullable=False)    
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True, index=True)  
    date_created = Column(DateTime, nullable=False, server_default=func.now())  
    date_updated = Column(DateTime, nullable=True, onupdate=func.now())

    movie = relationship("Movie", back_populates="comments", lazy='selectin') 
    user = relationship("User", back_populates="comments", lazy='selectin') 
    replies = relationship("Comment", back_populates="parent", lazy="selectin", cascade="all, delete-orphan")

    parent = relationship("Comment", remote_side=[id], back_populates="replies")

    def __repr__(self):
        return f"<Comment(content={self.content}, id={self.id}, parent_id={self.parent_id})>"