from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundError
from src.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository:
    pass


class BaseDBRepository(BaseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class BaseDBRepositoryWithModel(BaseDBRepository, Generic[T]):
    model: type[T]

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

        if not self.model or self.model is None:
            error_text = "Model must be specified in the repository."
            raise TypeError(error_text)

    async def get(self, **filters: Any) -> T | None:
        result = await self.session.scalars(select(self.model).filter_by(**filters))
        return result.first()

    async def get_all(
        self, limit: int | None = None, offset: int | None = None, **filters: Any
    ) -> tuple[int, Sequence[T]]:
        result = await self.session.scalars(
            select(self.model).filter_by(**filters).limit(limit).offset(offset)
        )
        total_count = await self.session.scalar(
            select(func.count(self.model.id)).filter_by(**filters)
        )
        return total_count, result.all()

    async def delete(self, **filters: Any) -> None:
        query = await self.session.execute(
            delete(self.model).filter_by(**filters).returning(self.model.id),
        )
        if not query.first():
            raise NotFoundError
