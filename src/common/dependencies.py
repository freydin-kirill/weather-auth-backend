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
    """Extract access token from the request."""

    if not token:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Return a user identified by the token."""

    username = verify_access_token(token)
    user = await UserDAO.find_one_or_none(email=username)
    if not user:
        raise UserNotFoundException
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Ensure that the user is active."""

    if current_user.is_active:
        return current_user
    raise UserInactiveException


async def get_user_permission(current_user: User = Depends(get_current_active_user)):
    """Ensure the user has administrative permissions."""

    if current_user.is_admin:
        return current_user
    raise ForbiddenException


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Create an asynchronous database session."""

    async with async_session_factory() as session:
        yield session


async def get_async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an asynchronous HTTP client."""

    async with AsyncClient() as client:
        yield client
