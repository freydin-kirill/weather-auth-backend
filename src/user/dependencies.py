from datetime import UTC, datetime

from fastapi import Depends, Request
from jwt import PyJWTError
from jwt import decode as jwt_decode

from src.config import settings
from src.exceptions import (
    ForbiddenException,
    TokenExpiredException,
    TokenInvalidException,
    TokenNotFoundException,
    UserInactiveException,
    UserNotFoundException,
)
from src.user.core import UserDAO
from src.user.models import User


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt_decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM])
    except PyJWTError:
        raise TokenInvalidException

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=UTC)
    if (not expire) or (expire_time < datetime.now(UTC)):
        raise TokenExpiredException

    user_id = payload.get("sub")
    if not user_id:
        raise UserNotFoundException

    user = await UserDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise UserNotFoundException

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    raise UserInactiveException


async def get_user_permission(current_user: User = Depends(get_current_active_user)):
    if current_user.is_admin:
        return current_user
    raise ForbiddenException
