from fastapi import APIRouter

from src.schemas.user import UserRead, UserUpdate
from src.auth.backend_jwt import fastapi_users

router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
