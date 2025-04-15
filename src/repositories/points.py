from typing import Any

from sqlalchemy import update

from src.core.exceptions import NotFoundError
from src.models.point import Point
from src.repositories.base import BaseDBRepositoryWithModel


class PointRepository(BaseDBRepositoryWithModel):
    model = Point

    async def create(self, **fields: Any) -> Point | None:
        point = Point(**fields)
        self.session.add(point)
        await self.session.commit()
        return point

    async def update(self, point_id: int, **fields: Any) -> Point | None:
        query = await self.session.scalars(
            update(Point).where(Point.id == point_id).values(**fields).returning(Point),
        )
        result = query.first()
        if not result:
            raise NotFoundError
        await self.session.commit()
        return result
