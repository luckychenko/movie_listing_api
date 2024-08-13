
from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import List, Optional
from datetime import datetime

from schemas import ResponseBase
from schemas.user_schema import UserOut



class CommentBase(BaseModel):
    content: str = Field(..., max_length=255, description="The Comment text)")

class CommentCreate(CommentBase):   
    movie_id: UUID4 = Field(..., description="The ID of the movie being commented")
    parent_id: Optional[int]  = Field(default=None, description="The ID of the parent comment, if any")

class CommentUpdate(CommentCreate):
     pass

class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The ID of the Comment")
    date_created: datetime 
    date_updated: Optional[datetime] 


class CommentOut(Comment):
    user: UserOut 
    parent_id: Optional[int] = None
    replies: List["CommentOut"] = []
    

class CommentResponse(ResponseBase):    
    data: Optional[CommentOut | List[CommentOut]] = None
