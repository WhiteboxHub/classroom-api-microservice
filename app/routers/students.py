from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.utils.security import decode_jwt_token

router = APIRouter(prefix="/students", tags=["Students"])

# Define the security scheme
security = HTTPBearer()

# Verify token dependency
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print("Token:", token)  # Debugging
    payload = decode_jwt_token(token)
    print("Decoded Payload:", payload)  # Debugging

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload

# Example of 403 Forbidden (e.g., admin-only endpoint)
def verify_admin(payload: dict = Depends(verify_token)):
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )

    return payload

@router.get("/")
def get_students(name: str = None, age: int = None, db: Session = Depends(get_db)):
    query = db.query(models.Student)

    if name:
        query = query.filter(models.Student.name.contains(name))
    if age:
        query = query.filter(models.Student.age == age)

    students = query.all()
    if not students:
        raise HTTPException(status_code=404, detail="No students found")

    return students

@router.post("/")
def add_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)  # Enforce token verification
):
    new_student = models.Student(name=student.name, age=student.age)

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {"message": "Student created successfully", "student": new_student}

# Example of an admin-only endpoint
@router.post("/admin-only")
def admin_only_endpoint(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_admin)  # Enforce admin verification
):
    return {"message": "This is an admin-only endpoint"}
