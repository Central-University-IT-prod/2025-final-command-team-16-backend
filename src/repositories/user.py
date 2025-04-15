from typing import Any

from src.models.user import User
from src.repositories.base import BaseDBRepositoryWithModel


class UserRepository(BaseDBRepositoryWithModel[User]):
    model = User

    async def create(self, **fields: Any) -> User:
        user = User(**fields)
        self.session.add(User)
        await self.session.commit()
        return user
