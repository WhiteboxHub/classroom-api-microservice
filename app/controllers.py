import json
from app.redis_client import db_redis
from app.database import get_db
from app.models import Student
from sqlalchemy.orm import Session

def get_all_students():
    """Fetch students from cache first, fallback to database if not found."""
    students = []
    keys = db_redis.keys("student:*")

    for key in keys:
        student_data = db_redis.get(key)
        if student_data:
            students.append(json.loads(student_data))

    if students:
        return students
    
    # If cache is empty, fetch from database
    with get_db() as db:
        students_from_db = db.query(Student).all()
        for student in students_from_db:
            student_dict = {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "class": student.class_name
            }
            db_redis.set(f"student:{student.id}", json.dumps(student_dict))
            students.append(student_dict)

    return students

def create_student(student_id: str, student_data: dict):
    """Store student in Redis cache."""
    key = f"student:{student_id}"
    db_redis.set(key, json.dumps(student_data))
    return student_data
