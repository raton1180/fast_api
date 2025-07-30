from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserData(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
        
class UsersResponse(BaseModel):
    status: int
    message: str
    data: List[UserData]

class UserResponse(BaseModel):
    status: int
    message: str
    data: UserData
class LoginResponseData(BaseModel):
    user: UserData
    access_token: str  # Added this field

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
     status: int
     message: str
     data: UserData
     access_token: str