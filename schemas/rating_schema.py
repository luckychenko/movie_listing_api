
from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional
# from uuid import UUID

class RatingBase(BaseModel):
    movie_id: int = Field(..., description="The ID of the movie being rated")
    user_id: int = Field(..., description="The ID of the user rating the movie")
    rating: float = Field(..., ge=0, le=10, description="The rating given to the movie (0-10)")

class RatingCreate(RatingBase):
    pass

class RatingUpdate(RatingBase):
    pass

class Rating(RatingBase):
    id: int = Field(..., description="The ID of the rating")

    class Config:
        model_config = ConfigDict(from_attributes=True)

class RatingResponse(Rating):
    pass