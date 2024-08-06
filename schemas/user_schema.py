from typing import List, Optional, Union
from pydantic import UUID4, BaseModel, ConfigDict , EmailStr, Field, field_validator

from schemas import ResponseBase



class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="User Email Address")
    full_name: Optional[str] = Field(default=None, max_length=255, description="User Fullname")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="User Email Address")
    password: str = Field(..., min_length=8, max_length=40, description="User secret password")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=40, description="User secret password")

class UserUpdate(UserCreate):
    pass
    # # email: Optional[EmailStr]  = Field(max_length=255, description="User Email Address")  # user shouldn't be able to change email address
    # full_name: str | None = Field(default=None, max_length=255, description="User Fullname")
    # password: str | None = Field(default=None, min_length=8, max_length=40, description="User secret password")

class UserInDB(UserBase):
    user_id: UUID4
    hashed_password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: UUID4


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    user_id: UUID4    


class UserResponse(ResponseBase):    
    data: Optional[Union[UserOut,List[UserOut]]] = None