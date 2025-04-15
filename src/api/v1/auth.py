from fastapi import APIRouter

from src.auth.backend_jwt import auth_backend, fastapi_users
from src.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt"
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

