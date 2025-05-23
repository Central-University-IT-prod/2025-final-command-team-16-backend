from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема пользователя."""


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления пользователя."""
