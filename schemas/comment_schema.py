
from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional
from datetime import datetime

# from sqlalchemy import UUID


class CommentBase(BaseModel):
    content: float = Field(..., max_length=255, description="The Comment text)")

class CommentCreate(CommentBase):   
    movie_id: str = Field(..., description="The ID of the movie being commented")
    user_id: str = Field(..., description="The ID of the user who comment the movie") 
    parent: Optional[int]  = Field(default=None, description="The ID of the parent comment, if any")
    # date_created: datetime = Field(..., default=datetime(), max_length=255, description="The Comment created date)")

class CommentUpdate(CommentCreate):
     pass

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The ID of the Comment")
    uuid: UUID4 = Field(..., description="The UUID of the Comment")
    date_created: datetime = Field(..., description="The date the comment was created")
    date_updated: Optional[datetime] = Field(None, description="The date the comment was last updated")



class CommentResponse(CommentBase):
    uuid: UUID4 = Field(..., description="The UUID of the comment")
    movie_id: int = Field(..., description="The ID of the movie")
    user_id: int = Field(..., description="The ID of the user")
    date_created: datetime = Field(..., description="The date the comment was created")
    date_updated: Optional[datetime] = Field(None, description="The date the comment was last updated")
    
class CommentsPublic(BaseModel):
    data: list[CommentResponse]
    count: int