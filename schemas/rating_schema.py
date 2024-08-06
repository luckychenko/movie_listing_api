
from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import Optional
# from uuid import UUID

class RatingBase(BaseModel):
    movie_id: int = Field(..., description="The ID of the movie being rated")
    score: float = Field(..., ge=0, le=10, description="The rating given to the movie (0-10)")

class RatingCreate(RatingBase):
    pass

class RatingUpdate(RatingBase):
    pass

class Rating(RatingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The ID of the rating")
    uuid: UUID4 = Field(..., description="The UUID of the Comment")
    user_id: int = Field(..., description="The ID of the user rating the movie")

class RatingResponse(RatingBase):    
    uuid: UUID4 = Field(..., description="The UUID of the Comment")
    user_id: int = Field(..., description="The ID of the user rating the movie")