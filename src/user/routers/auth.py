from fastapi import APIRouter
from starlette.responses import Response

from src.common.exceptions import UserAlreadyExistsException, UserEmailOrPasswordException, UserInactiveException
from src.user.core.hashing import get_hashed_password, verify_password
from src.user.core.security import create_access_token
from src.user.crud import UserDAO
from src.user.schemas import SUserLogin, SUserRegister


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
    await UserDAO.create(**user_dict)
    return {"message": "User registered successfully"}


@router.post("/login/")
async def login_user(response: Response, user_data: SUserLogin):
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if not user or not verify_password(user_data.password, user.password):
        raise UserEmailOrPasswordException
    if not user.is_active:
        raise UserInactiveException
    access_token = create_access_token(subject=str(user.id))
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Logout successfully"}
