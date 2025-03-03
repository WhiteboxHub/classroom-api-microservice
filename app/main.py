from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routers import students, auth, profiles
from app.database import init_db, mongo_client
from app.utils.api_gateway import APIGateway  # Import APIGateway class

app = FastAPI()
api_gateway = APIGateway()  # Create an instance of APIGateway

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()  # Initialize MySQL database tables

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
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(profiles.router)

@app.get("/")
@api_gateway.rate_limited(max_calls=10, time_frame=60)  # Apply rate limiting
async def root(request: Request):
    return {"message": "Student Microservice Running"}
