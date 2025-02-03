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


# Pydantic Model for MongoDB (Social Profiles)
class SocialLinks(BaseModel):
    facebook: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    twitter: Optional[HttpUrl] = None

class StudentProfile(BaseModel):
    student_id: int
    name: str
    social_links: Optional[SocialLinks] = None

    class Config:
        orm_mode = True

