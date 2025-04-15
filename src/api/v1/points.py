from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Response, status

from src.core.exceptions import NotFoundError
from src.db.manager import SessionDependency
from src.repositories.points import PointRepository
from src.schemas.point import Point, PointCreate

router = APIRouter(prefix="/points", tags=["Points"])


@router.post("", response_model=Point)
async def create_point_handler(
    point_create: PointCreate,
    session: SessionDependency,
) -> Point | None:
    point_repository = PointRepository(session)
    return await point_repository.create(**point_create.model_dump())


@router.get("", response_model=list[Point])
async def get_points_handler(
    session: SessionDependency,
    response: Response,
) -> Sequence[Point]:
    point_repository = PointRepository(session)
    total_count, result = await point_repository.get_all()
    response.headers["X-Total-Count"] = str(total_count)
    return result


@router.get("/{pointId}", response_model=Point)
async def get_point_handler(
    point_id: Annotated[int, Path(alias="pointId")],
    session: SessionDependency,
) -> Point | None:
    point_repository = PointRepository(session)
    try:
        return await point_repository.get(id=point_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Point not found",
        ) from e


@router.patch("/{pointId}", response_model=Point)
async def update_point_handler(
    point_id: Annotated[int, Path(alias="pointId")],
    point_update: PointCreate,
    session: SessionDependency,
) -> Point | None:
    point_repository = PointRepository(session)
    try:
        return await point_repository.update(point_id, **point_update.model_dump())
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Point not found",
        ) from e


@router.delete("/{pointId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_point_handler(
    point_id: Annotated[int, Path(alias="pointId")],
    session: SessionDependency,
) -> None:
    point_repository = PointRepository(session)
    try:
        await point_repository.delete(id=point_id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Point not found",
        ) from e
