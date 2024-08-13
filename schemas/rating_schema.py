
from pydantic import BaseModel, ConfigDict, Field, UUID4
from typing import List, Optional
from schemas import ResponseBase
from schemas.user_schema import UserOut

class RatingBase(BaseModel):
    score: float = Field(..., ge=0, le=10, description="The rating given to the movie (0-10)")

class RatingCreate(RatingBase):
    movie_id: UUID4 = Field(..., description="The ID of the movie being rated")
    

class RatingUpdate(RatingBase):
    movie_id: UUID4 = Field(..., description="The ID of the movie being rated")
    
class Rating(RatingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The ID of the rating")
    ruid: UUID4 = Field(..., description="The UUID of the Comment")
    user_id: int = Field(..., description="The ID of the user rating the movie")

class RatingOut(RatingBase):  
    ruid: UUID4 
    movie_id: UUID4 
    score: Optional[float] = None
    user: UserOut

class RatingScoreOut(BaseModel):
    movie_id: UUID4 
    total_ratings: int
    avg_ratings_score: Optional[float] = None

class RatingResponse(ResponseBase):    
    data: Optional[RatingOut | List[RatingOut] | RatingScoreOut] = None