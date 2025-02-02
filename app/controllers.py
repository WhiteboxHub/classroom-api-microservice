from sqlalchemy.orm import Session
from app.models import Student

def get_all_students(db: Session):
    return db.query(Student).all()

def create_student(db: Session, student: Student):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
