from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import StudentCreate
from app.controllers import get_all_students, create_student

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/")
def get_students(db: Session = Depends(get_db)): # removed this payload: dict = Depends(verify_token)
    """Fetch students using the controller (cache-first approach)."""
    students = get_all_students(db)
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

  # Import the correct Pydantic model

@router.post("/")
def add_student(student: StudentCreate):  # ✅ Use Pydantic model
    """Create a student and store in Redis."""
    
    student_id = student.id  # ✅ Access attribute directly instead of using .get()
    
    if not student_id:
        raise HTTPException(status_code=400, detail="Student ID is required")
    
    new_student = create_student(student_id, student.dict())  # ✅ Convert Pydantic model to dict
    return {"message": "Student created successfully", "student": new_student}

