from fastapi import APIRouter, Depends, Response
from pydantic import EmailStr

from src.exceptions import (
    UserAlreadyExistsException,
    UserEmailOrPasswordException,
    UserInactiveException,
)
from src.user.auth import authenticate_user, create_access_token, get_hashed_password
from src.user.core import UserDAO
from src.user.dependencies import get_current_active_user, get_user_permission
from src.user.models import User
from src.user.schemas import SUserAuth, SUserRegister


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.model_dump()
    user_dict["password"] = get_hashed_password(user_data.password)
    await UserDAO.add(**user_dict)
    return {"message": "User registered successfully"}


@router.post("/login/")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(email=user_data.email, password=user_data.password)
    if user is None:
        raise UserEmailOrPasswordException
    if not user.is_active:
        raise UserInactiveException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Logout successfully"}


@router.post("/delete/")
async def delete_user(user_id: int, admin: User = Depends(get_user_permission)):
    return await UserDAO.delete(item_id=user_id)


@router.post("/update/role/")
async def change_user_role(user_id: int, is_admin: bool = False, admin: User = Depends(get_user_permission)):
    return await UserDAO.update(item_id=user_id, is_admin=is_admin)


@router.post("/update/active/")
async def change_user_active_status(user_id: int, is_active: bool = False, admin: User = Depends(get_user_permission)):
    return await UserDAO.update(item_id=user_id, is_active=is_active)


@router.post("/update/password/")
async def change_user_password(new_password: str, user: User = Depends(get_current_active_user)):
    return await UserDAO.update(item_id=user.id, password=get_hashed_password(new_password))


@router.post("/update/email/")
async def change_user_email(new_email: EmailStr, user: User = Depends(get_current_active_user)):
    existing_user = await UserDAO.find_one_or_none(email=new_email)
    if existing_user:
        raise UserAlreadyExistsException
    return await UserDAO.update(item_id=user.id, email=new_email)


@router.get("/me/")
async def get_me(user: User = Depends(get_current_active_user)):
    return user
