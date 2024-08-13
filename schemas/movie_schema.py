from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, ConfigDict , Field, UUID4

from schemas import ResponseBase
from schemas.user_schema import UserOut
# from uuid import UUID

class MovieBase(BaseModel):
    title: str = Field(..., max_length=255, description="The movie title")
    description: Optional[str] = Field(default=None, max_length=255, description="The movie description")
    
class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    title: Optional[str] = Field(..., max_length=255, description="The movie title")
    

class Movie(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    muid: UUID4
    

class MovieOut(MovieBase):
    muid: UUID4
    # rating: Optional[int] = None
    date_created: datetime
    date_updated: Optional[datetime] = None
    user: UserOut

    
    model_config = ConfigDict(from_attributes=True)

class MovieResponse(ResponseBase):    
    data: Optional[MovieOut | List[MovieOut]] = None
    
