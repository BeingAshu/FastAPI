from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from pathlib import Path

# Load the .env file from the auth_service folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)


# Get database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")


# Create database engine
engine = create_engine(DATABASE_URL)




# # PostgreSQL connection URL
# db_url = "postgresql://postgres:12345678@localhost:5432/fastapi-users"

# # Create database engine
# engine = create_engine(db_url)    #Establishes the database connection configuration

# Create database session
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


# Database dependency for FastAPI
def get_db():                                     # Provides a session to an API request and closes it afterward
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()