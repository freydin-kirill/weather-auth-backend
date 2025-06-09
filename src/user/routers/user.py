from fastapi import APIRouter, Depends
from pydantic import EmailStr

from src.common.dependencies import get_current_active_user
from src.common.exceptions import UserAlreadyExistsException
from src.user.core.hashing import get_hashed_password
from src.user.crud import UserDAO
from src.user.models import User
from src.user.schemas import SUserRead


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/me/", response_model=SUserRead)
async def get_me(user: User = Depends(get_current_active_user)):
    return user


@router.post("/update/password/")
async def change_user_password(new_password: str, user: User = Depends(get_current_active_user)):
    return await UserDAO.update(item_id=user.id, password=get_hashed_password(new_password))


@router.post("/update/email/")
async def change_user_email(new_email: EmailStr, user: User = Depends(get_current_active_user)):
    existing_user = await UserDAO.find_one_or_none(email=new_email)
    if existing_user:
        raise UserAlreadyExistsException
    return await UserDAO.update(item_id=user.id, email=new_email)
