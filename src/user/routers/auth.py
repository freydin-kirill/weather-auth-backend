from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.common.exceptions import (
    UserAlreadyExistsException,
    UserEmailOrPasswordException,
    UserInactiveException,
)
from src.user.core.hashing import get_hashed_password, verify_password
from src.user.core.security import create_access_token
from src.user.crud import UserDAO
from src.user.schemas import SUserRegister, Token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register/")
async def register(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    user_dict = user_data.model_dump()
    user_dict["password"] = get_hashed_password(user_data.password)
    await UserDAO.create(**user_dict)
    return {"message": "User registered successfully"}


@router.post("/login/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserDAO.find_one_or_none(email=form_data.username)
    if not user or not verify_password(form_data.password, str(user.password)):
        raise UserEmailOrPasswordException
    if not user.is_active:
        raise UserInactiveException
    access_token = create_access_token(subject=str(user.email))
    return Token(access_token=access_token, token_type="bearer")
