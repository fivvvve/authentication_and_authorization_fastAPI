from fastapi import Response
from fastapi.security import APIKeyCookie

import jwt
from passlib.context import CryptContext
from dataclasses import dataclass, asdict

from datetime import datetime, timedelta, timezone

from .env import env
from models.user import UserProfile

ALGORITHM = "HS256"
COOKIE_NAME = "authToken"

# Using APIKeyCookie for better UI on Swagger, showing private routes
cookie_scheme = APIKeyCookie(name=COOKIE_NAME, auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: UserProfile):
    encoded_jwt = jwt.encode(asdict(data), env.JWT_SECRET, algorithm=ALGORITHM)
    
    return encoded_jwt


@dataclass
class VerifyJWTResponse:
    valid: bool
    user: UserProfile | None = None

def verify_token(token: str) -> VerifyJWTResponse:
    try:
        payload = jwt.decode(token, env.JWT_SECRET, algorithms=[ALGORITHM])
        userData = UserProfile(email=payload['email'], type=payload['type'])
        return VerifyJWTResponse(valid=True, user=userData)
    except jwt.PyJWTError:
        return VerifyJWTResponse(valid=False, user=None)


def set_jwt_cookie(response: Response, token: str):
    is_development = env.ENVIRONMENT.lower() == "development"

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False if is_development else True,
        samesite="lax" if is_development else "none",
        max_age=env.JWT_COOKIE_EXPIRE_MINUTES * 60,
        expires=datetime.now(timezone.utc) + timedelta(minutes=env.JWT_COOKIE_EXPIRE_MINUTES)
    )


def remove_jwt_cookie(response: Response):
    is_development = env.ENVIRONMENT.lower() == "development"

    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=True,
        secure=False if is_development else True,
        samesite="lax" if is_development else "none"
    )