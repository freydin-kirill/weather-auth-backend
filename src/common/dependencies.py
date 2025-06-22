from collections.abc import AsyncGenerator

from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.exceptions import (
    ForbiddenException,
    TokenNotFoundException,
    UserInactiveException,
    UserNotFoundException,
)
from src.db.session import async_session_factory
from src.user.core.security import oauth2_scheme, verify_access_token
from src.user.crud import UserDAO
from src.user.models import User


def get_token(token: str = Depends(oauth2_scheme)):
    if not token:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    username = verify_access_token(token)
    user = await UserDAO.find_one_or_none(email=username)
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


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


async def get_async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient() as client:
        yield client
