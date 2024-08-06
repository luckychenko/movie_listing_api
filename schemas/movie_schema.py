from typing import Optional
from pydantic import BaseModel, ConfigDict , Field, UUID4
# from uuid import UUID

class MovieBase(BaseModel):
    title: str = Field(..., max_length=255, description="The movie title")
    description: Optional[str] = Field(default=None, max_length=255, description="The movie description")
    
class MovieCreate(MovieBase):
    user_id: int

class MovieUpdate(MovieBase):
    uuid: UUID4
    user_id: int

class Movie(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uuid: UUID4
    

class MovieResponse(MovieUpdate):
    rating: int

class MoviesPublic(BaseModel):
    data: list[MovieResponse]
    count: int