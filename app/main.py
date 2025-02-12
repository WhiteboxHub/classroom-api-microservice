import time
from functools import wraps
from fastapi import FastAPI, Request, HTTPException, status
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

init_db()  # Initialize MySQL database tables

# Rate Limiting Decorator
def rate_limited(max_calls: int, time_frame: int):
    """
    Rate limit decorator to restrict the number of API calls in a given time frame.
    :param max_calls: Maximum number of calls allowed in the time frame.
    :param time_frame: The time frame (in seconds) for rate limiting.
    :return: Decorator function.
    """
    calls = []  # Store timestamps of API requests

    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time.time()
            nonlocal calls
            # Keep only calls within the time frame
            calls = [call for call in calls if now - call < time_frame]

            if len(calls) >= max_calls:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please try again later."
                )

            calls.append(now)
            return await func(request, *args, **kwargs)

        return wrapper
    return decorator

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

# Include Routers with Rate Limiting
app.include_router(students.router)
app.include_router(profiles.router)

@app.get("/")
@rate_limited(max_calls=10, time_frame=60)  # Rate limit: 10 requests per 60 seconds
async def root(request: Request):
    return {"message": "Student Microservice Running"}
