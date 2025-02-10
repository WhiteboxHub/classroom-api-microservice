from fastapi import APIRouter, Depends, HTTPException
# from app.auth import verify_token
from app.controllers import get_student_profile, create_student_profile
from app.models import StudentProfile

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/{student_id}")
async def get_profile(student_id: int): # removed this  payload: dict = Depends(verify_token)
    """Fetch a student's social profile from MongoDB"""
    profile = await get_student_profile(student_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/")
async def add_profile(profile: StudentProfile): # removed this  payload: dict = Depends(verify_token)
    """Create a student's social profile in MongoDB"""
    new_profile = await create_student_profile(profile)
    return {"message": "Profile created successfully", "profile": new_profile}

