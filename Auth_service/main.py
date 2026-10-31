from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import database_models
from .models import RegisterUser, LoginUser, UserResponse, TokenResponse
from .security import (
    hash_password,
    verify_password,
    create_access_token
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield

app = FastAPI(
    title="Authentication Microservice",
    description="User registration and login APIs",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registration API
@app.post(
    "/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: RegisterUser, db: Session = Depends(get_db)):

    existing_user = db.query(database_models.AuthUsers).filter(
        database_models.AuthUsers.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = database_models.AuthUsers(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Login API
@app.post("/auth/login", response_model=TokenResponse)
def login_user(user: LoginUser, db: Session = Depends(get_db)):

    db_user = db.query(database_models.AuthUsers).filter(
        database_models.AuthUsers.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not db_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Get current authenticated user's basic account information
@app.get("/auth/me", response_model=UserResponse)
def get_current_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    db_user = db.query(database_models.AuthUsers).filter(
        database_models.AuthUsers.id == user_id
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return db_user
