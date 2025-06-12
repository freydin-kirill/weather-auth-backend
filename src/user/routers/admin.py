from fastapi import APIRouter, Depends

from src.common.dependencies import get_user_permission
from src.user.crud import UserDAO
from src.user.models import User


router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


@router.get("/get_all_users/")
async def get_all_users(admin: User = Depends(get_user_permission)):
    return await UserDAO.find_all()


@router.post("/delete_user/")
async def delete_user(user_id: int, admin: User = Depends(get_user_permission)):
    return await UserDAO.delete(item_id=user_id)


@router.post("/change_user_role/")
async def change_user_role(user_id: int, is_admin: bool = False, admin: User = Depends(get_user_permission)):
    return await UserDAO.update(item_id=user_id, is_admin=is_admin)


@router.post("/change_user_active_status/")
async def change_user_active_status(user_id: int, is_active: bool = False, admin: User = Depends(get_user_permission)):
    return await UserDAO.update(item_id=user_id, is_active=is_active)
