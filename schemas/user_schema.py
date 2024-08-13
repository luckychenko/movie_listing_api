from typing import List, Optional, Union
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import UUID4, BaseModel, ConfigDict , EmailStr, Field, field_validator

from schemas import ResponseBase



class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255, description="User Email Address")
    full_name: Optional[str] = Field(default=None, max_length=255, description="User Fullname")

class UserLogin(OAuth2PasswordRequestForm):     
     def __init__(
        self, 
        username: EmailStr = Form(..., max_length=255, description="User Email Address", title="Email Address"), # used alias=username to mimic OAuth2PasswordBearer
        password: str = Form(..., min_length=8, max_length=40, description="User secret password"), 
        scope: str = Form(""),
        client_id: str = Form(None),
        client_secret: str = Form(None)
    ):
        self.username = username 
        self.password = password
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
    
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=40, description="User secret password")

class UserUpdate(UserCreate):
    pass

class UserInDB(UserBase):
    uid: UUID4
    hashed_password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    uid: UUID4


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    uid: UUID4    


class UserResponse(ResponseBase):    
    data: Optional[Union[UserOut,List[UserOut]]] = None