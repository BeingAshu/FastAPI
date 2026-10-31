
import os
from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash


# Password hashing
password_hash = PasswordHash.recommended()


# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not configured")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Hash password
def hash_password(password: str):

    return password_hash.hash(password)


# Verify password
def verify_password(plain_password: str, hashed_password: str):

    return password_hash.verify(plain_password, hashed_password)


# Generate JWT token
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
