from datetime import UTC, datetime, timedelta

from fastapi.security import HTTPBearer
from jwt import ExpiredSignatureError, PyJWTError
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from src.common.exceptions import TokenExpiredException, TokenInvalidException, UserNotFoundException
from src.config import settings


# TODO: Add JWT authentication support
security = HTTPBearer()


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if not expires_delta:
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(UTC) + expires_delta
    payload = {"exp": expire, "sub": subject}
    encoded_jwt = jwt_encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> str:
    try:
        payload = jwt_decode(jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except PyJWTError:
        raise TokenInvalidException

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=UTC)
    if (not expire) or (expire_time < datetime.now(UTC)):
        raise TokenExpiredException

    user_id = payload.get("sub")
    if not user_id:
        raise UserNotFoundException

    return user_id


# TODO: Add refresh token support
def refresh_access_token(token: str) -> str:
    pass
