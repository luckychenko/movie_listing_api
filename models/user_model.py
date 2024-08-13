from sqlalchemy import Column, String, Integer, UUID
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID
from core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    uid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)

    movies = relationship("Movie", back_populates="user", cascade="all, delete-orphan", lazy="selectin") 
    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan", lazy="selectin") 
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan", lazy="selectin")  