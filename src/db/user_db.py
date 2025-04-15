from collections.abc import AsyncGenerator

from fastapi_users.db import SQLAlchemyUserDatabase

from src.db.manager import SessionDependency
from src.models.user import User


async def get_user_db(
    session: SessionDependency,
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)
