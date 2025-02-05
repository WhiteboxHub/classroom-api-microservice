from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
# from app.auth import verify_token
from app.controllers import get_all_students, create_student

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/")
def get_students(): # removed this payload: dict = Depends(verify_token)
    """Fetch students using the controller (cache-first approach)."""
    students = get_all_students()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return students

@router.post("/")
def add_student(student: dict ): # removed this payload: dict = Depends(verify_token)
    """Create a student and store in Redis."""
    student_id = student.get("id")
    if not student_id:
        raise HTTPException(status_code=400, detail="Student ID is required")
    
    new_student = create_student(student_id, student)
    return {"message": "Student created successfully", "student": new_student}
