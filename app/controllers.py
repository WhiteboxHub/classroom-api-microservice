import json
from app.redis_client import db_redis
from app.database import get_db, get_mongo_collection
from app.models import Student, StudentProfile
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

# MongoDB Collection
mongo_collection = get_mongo_collection("students")


def get_all_students(db: Session, name: str = None, age: int = None):
    """Fetch students from cache first, fallback to database if not found, with optional filtering."""
    students = []
    
    # Fetching keys from the cache for 'student:*'
    keys = db_redis.keys("student:*")

    # If cache has data, filter based on name and age
    for key in keys:
        student_data = db_redis.get(key)
        if student_data:
            student_dict = json.loads(student_data)
            
            # Apply name and age filtering if provided
            name_match = not name or name.lower() in student_dict['name'].lower()
            age_match = not age or student_dict['age'] == age

            if name_match and age_match:
                students.append(student_dict)
    
    # If we have results from cache, return them
    if students:
        return students
    
    # If cache is empty or no match, fetch from MySQL database
    query = db.query(Student)
    
    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))  # Partial match for name
    if age:
        query = query.filter(Student.age == age)  # Exact match for age
    
    students_from_db = query.all()

    # Store fetched students in the cache and return them
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

