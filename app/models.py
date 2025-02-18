from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# SQLAlchemy Model for MySQL



class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    phone_number: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(Base):
    __tablename__ = "auth"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=True)
    role = Column(String, default="user") 
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String)


class StudentCreate(BaseModel):
    id: int
    name: str
    age: int
    grade: str


    class Config:
        orm_mode = True
        
# Pydantic Model for MongoDB (Social Profiles)
class SocialLinks(BaseModel):
    facebook: Optional[str] = None  # ✅ Store as plain string
    linkedin: Optional[str] = None
    twitter: Optional[str] = None


class StudentProfile(BaseModel):
    student_id: int
    name: str
    social_links: Optional[SocialLinks] = None

    @field_validator("name")
    @classmethod
    def name_must_be_alpha(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters Not Even spaces too")
        return value

    class Config:
        orm_mode = True