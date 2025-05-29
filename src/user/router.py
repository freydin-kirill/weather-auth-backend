from fastapi import APIRouter, Response

from src.exceptions import UserAlreadyExistsException, UserEmailOrPasswordException
from src.user.auth import authenticate_user, create_access_token, get_hashed_password
from src.user.core import UserDAO
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
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise UserEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Logout successfully"}
