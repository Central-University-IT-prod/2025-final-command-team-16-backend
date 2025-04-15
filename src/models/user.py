from fastapi_users.db import SQLAlchemyBaseUserTable

from src.models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):  # type: ignore[misc]
    pass
