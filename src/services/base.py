from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from src.core.exceptions import NotFoundError
from src.repositories.base import (
    BaseDBRepositoryWithModel,
    BaseRepository,
)
from src.repositories.manager import RepositoryManager

T = TypeVar("T", bound=BaseModel)
T_repo = TypeVar("T_repo", bound=BaseDBRepositoryWithModel[Any])


class BaseDBService(Generic[T, T_repo]):
    schema: type[T]

    def __init__(
        self,
        repository_manager: RepositoryManager,
        repository: T_repo,
    ) -> None:
        self.repository_manager = repository_manager
        self.repository = repository

    async def get(self, **filters: Any) -> T:
        result = await self.repository.get(**filters)
        if not result:
            raise NotFoundError
        return self.schema.model_validate(result)

    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters: Any,
    ) -> tuple[int, list[T]]:
        total_count, result = await self.repository.get_all(limit, offset, **filters)
        return total_count, [self.schema.model_validate(item) for item in result]

    async def delete(self, **filters: Any) -> None:
        await self.repository.delete(**filters)


class BaseService:
    repository: type[BaseRepository]
