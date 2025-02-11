from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import students, profiles
from app.database import init_db, mongo_client

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
# Initialize MySQL database tables

@app.on_event("startup")
async def startup_db_client():
    """Ensure MongoDB connection is active on startup"""
    try:
        mongo_client.admin.command("ping")
        print("✅ MongoDB Connected Successfully!")
        
    except Exception as e:
        print(f"❌ MongoDB Connection Error: {e}")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on shutdown"""
    mongo_client.close()

# Include Routers

app.include_router(students.router)
app.include_router(profiles.router)  # Added profiles router for MongoDB profiles

@app.get("/")
def root():
    return {"message": "Student Microservice Running"}

