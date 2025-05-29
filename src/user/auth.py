from datetime import UTC, datetime, timedelta

from fastapi.security import HTTPBearer
from jwt import encode as jwt_encode
from passlib.context import CryptContext
from pydantic import EmailStr

from src.config import settings
from src.user.core import UserDAO


security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    if not expires_delta:
        expires_delta = timedelta(minutes=15)
    expire = datetime.now(UTC) + expires_delta
    payload = data.copy()
    payload.update({"exp": expire})
    encoded_jwt = jwt_encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str | EmailStr, password: str):
    user = await UserDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.password):
        return None
    return user
