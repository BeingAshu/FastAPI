from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
db_url = "postgresql://postgres:12345678@localhost:5432/fastapi-users"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)