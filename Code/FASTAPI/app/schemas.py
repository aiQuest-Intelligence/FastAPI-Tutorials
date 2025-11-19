from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import datetime
from typing import Optional

#define request body schema
class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl

class CourseResponse(CourseCreate):
    id : int

    class Config:
        orm_model = True
# class CourseResponse(BaseModel):
#     name: str
#     instructor: str

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserRes(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_model = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[int] = None