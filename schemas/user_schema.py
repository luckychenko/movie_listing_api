from pydantic import BaseModel, ConfigDict , EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255) 
    password: str | None = Field(default=None, min_length=8, max_length=40)

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    pass

class UsersPublic(BaseModel):
    data: list[User]
    count: int