from typing import Optional
from uuid import UUID
from pydantic import UUID4, BaseModel, ConfigDict , EmailStr, Field



class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="User Email Adrress")
    full_name: Optional[str] = Field(default=None, max_length=255, description="User Fullname")

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40, description="User secret password")

class UserUpdate(UserCreate):
    pass
    # # email: Optional[EmailStr]  = Field(max_length=255, description="User Email Address")  # user shouldn't be able to change email address
    # full_name: str | None = Field(default=None, max_length=255, description="User Fullname")
    # password: str | None = Field(default=None, min_length=8, max_length=40, description="User secret password")

class UserInDB(UserBase):
    user_id: UUID4
    hashed_password: str

class User(UserBase):
    id: int
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    user_id: UUID

class UsersPublic(BaseModel):
    data: list[UserResponse]
    count: int