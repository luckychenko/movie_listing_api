
from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import List, Optional
from datetime import datetime

from schemas import ResponseBase

# from sqlalchemy import UUID


class CommentBase(BaseModel):
    content: float = Field(..., max_length=255, description="The Comment text)")

class CommentCreate(CommentBase):   
    movie_id: str = Field(..., description="The ID of the movie being commented")
    # user_id: str = Field(..., description="The ID of the user who comment the movie") 
    parent_id: Optional[int]  = Field(default=0, description="The ID of the parent comment, if any")
    # date_created: datetime = Field(..., default=datetime(), max_length=255, description="The Comment created date)")

class CommentUpdate(CommentCreate):
     pass

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The ID of the Comment")
    cuid: UUID4 = Field(..., description="The UUID of the Comment")
    date_created: datetime = Field(..., description="The date the comment was created")
    date_updated: Optional[datetime] = Field(None, description="The date the comment was last updated")


class CommentOut(CommentBase):
    cuid: UUID4 
    movie_id: UUID4 
    user_id: UUID4 
    parent_id: Optional[int] = None
    replies: List["CommentOut"] = []
    date_created: datetime 
    date_updated: Optional[datetime] 
    

class CommentResponse(ResponseBase):    
    data: Optional[CommentOut | List[CommentOut]] = None
