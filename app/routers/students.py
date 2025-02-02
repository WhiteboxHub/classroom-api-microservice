from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Student
from app.auth import verify_token

router = APIRouter(prefix="/students", tags=["students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.post("/")
def create_student(student: Student, db: Session = Depends(get_db)):
    db.add(student)
    db.commit()
    return student
