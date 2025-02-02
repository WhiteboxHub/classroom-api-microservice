from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import students, auth
from app.database import init_db

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include Routers
app.include_router(auth.router)
app.include_router(students.router)

@app.get("/")
def root():
    return {"message": "Student Microservice Running"}
