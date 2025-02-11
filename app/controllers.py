import json
from app.redis_client import db_redis
from app.database import get_db, get_mongo_collection
from app.models import Student, StudentProfile
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

# MongoDB Collection
mongo_collection = get_mongo_collection("students")


# 🟢 Fetch all students (Redis + MySQL)
def get_all_students(db: Session):
    """Fetch students from cache first, fallback to database if not found."""
    students = []
    keys = db_redis.keys("student:*")
    

    for key in keys:
        student_data = db_redis.get(key)
        if student_data:
            students.append(json.loads(student_data))

    if students:
        return students
    
    # If cache is empty, fetch from MySQL database
   
    students_from_db = db.query(Student).all()
    for student in students_from_db:
            student_dict = {
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "class": student.grade  # Fixed class -> grade
            }
            db_redis.set(f"student:{student.id}", json.dumps(student_dict))
            students.append(student_dict)

    return students


# 🟢 Create a student (Redis)
def create_student(student_id: str, student_data: dict):
    """Store student in Redis cache."""
    key = f"student:{student_id}"
    db_redis.set(key, json.dumps(student_data))
    return student_data


# 🔵 Fetch a student's social profile (MongoDB)
async def get_student_profile(student_id: int):
    """Retrieve a student's social profile from MongoDB"""
    profile = await mongo_collection.find_one({"student_id": student_id}, {"_id": 0})
    return profile


# 🔵 Create a student's social profile (MongoDB)
async def create_student_profile(profile: StudentProfile):
    """Create a student's social profile in MongoDB"""
    existing_profile = await mongo_collection.find_one({"student_id": profile.student_id})
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    new_profile = jsonable_encoder(profile.dict())  # ✅ Handles serialization
    result = await mongo_collection.insert_one(new_profile)
    
    new_profile["_id"] = str(result.inserted_id)  # ✅ Ensure `_id` is a string

    return new_profile
