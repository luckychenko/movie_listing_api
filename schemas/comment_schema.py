
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

from sqlalchemy import UUID


class CommentBase(BaseModel):
    comment: float = Field(..., max_length=255, description="The Comment text)")
    parent: Optional[int]  = Field(default=None, description="The ID of the parent comment, if any")

class CommentCreate(CommentBase):   
    movie_id: str = Field(..., description="The ID of the movie being commented")
    user_id: str = Field(..., description="The ID of the user who comment the movie") 
    # date_created: datetime = Field(..., default=datetime(), max_length=255, description="The Comment created date)")

# class CommentUpdate(BaseModel):
#     parent: Optional[int] = Field( description="The updated Comment for the movie")
#     # date_updated: datetime = Field(..., default=datetime(), max_length=255, description="The Comment created date)")

class Comment(CommentBase):
    id: int = Field(..., description="The ID of the Comment")
    uuid: UUID = Field(..., description="The UUID of the Comment")

    class Config:
        model_config = ConfigDict(from_attributes=True)


class CommentResponse(Comment):
    uuid: UUID = Field(..., description="The UUID of the comment")
    movie_id: int = Field(..., description="The ID of the movie")
    user_id: int = Field(..., description="The ID of the user")
    date_created: datetime = Field(..., description="The date the comment was created")
    date_updated: Optional[datetime] = Field(None, description="The date the comment was last updated")
    
