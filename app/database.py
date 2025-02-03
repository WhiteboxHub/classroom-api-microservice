from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

# MySQL Database Connection
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@mysql/student_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Initialize MySQL database tables"""
    Base.metadata.create_all(bind=engine)

# MongoDB Database Connection
MONGODB_URL = "mongodb://mongodb:27017"
mongo_client = AsyncIOMotorClient(MONGODB_URL)
mongo_db = mongo_client["social_profiles"]  # MongoDB database

def get_mongo_collection(collection_name: str):
    """Returns a MongoDB collection"""
    return mongo_db[collection_name]
