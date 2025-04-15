from src.core.exceptions import NotFoundError
from src.repositories import PointRepository
from src.schemas import Point, PointCreate, PointUpdate
from src.services.base import BaseDBService


class PointService(BaseDBService[Point, PointRepository]):
    schema = Point

    async def create(self, point_create: PointCreate) -> Point:
        result = await self.repository.create(**point_create.model_dump())
        if result is None:
            raise NotFoundError
        return result

    async def update(self, point_id: int, point_update: PointUpdate) -> Point:
        result = await self.repository.update(point_id, **point_update.model_dump())
        if result is None:
            raise NotFoundError
        return result
