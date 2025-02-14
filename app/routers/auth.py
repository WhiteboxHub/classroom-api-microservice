from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.utils.security import hash_password, verify_password, create_jwt_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register_user(user: schemas.UserRegister, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        email=user.email,
        username=user.username,
        password_hash=hashed_password,
        role=user.role 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully!"}

@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_jwt_token(db_user.email, db_user.role)
    return {"message": "Login successful", "token": token}
