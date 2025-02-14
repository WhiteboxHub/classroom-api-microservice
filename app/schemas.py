from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# User Registration Schema
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    phone_number: Optional[str] = None
    role: Optional[str] = "user"

# User Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class TokenData(BaseModel):
    email: str
    is_admin: bool

# Student Schemas
class StudentCreate(BaseModel):
    name: str
    age: int
