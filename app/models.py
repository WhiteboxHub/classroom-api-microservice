from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel, field_validator
from typing import Optional

# SQLAlchemy Model for MySQL
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

    @field_validator('name')
    def name_must_be_alpha(cls, value):
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value

    @field_validator('age')
    def age_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Age must be a positive integer")
        return value

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

    class Config:
        orm_mode = True

