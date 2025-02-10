from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel, HttpUrl
from typing import Optional

# SQLAlchemy Model for MySQL
class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String)


class StudentCreate(BaseModel):
    id: str
    name: str
    age: int
    grade: str

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

