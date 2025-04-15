import json
from collections.abc import Sequence
from typing import Annotated

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Path,
    Query,
    Response,
    UploadFile,
    status,
)
from fastapi.exceptions import RequestValidationError
from pydantic_core._pydantic_core import ValidationError

from src.core.exceptions import NotFoundError
from src.db.manager import SessionDependency
from src.repositories import BookMainImageRepository, BookRepository, PointRepository
from src.repositories.manager import RepositoryManager
from src.schemas.book_offer import BookOffer, BookOfferCreate, BookOfferUpdate
from src.services.book_offer import BookOfferService
from src.utils.files import get_file_url, save_uploaded_file

router = APIRouter(prefix="/book-offer", tags=["Book-offer"])


@router.get("/")
async def get_book_offers(
    session: SessionDependency,
    response: Response,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=0)] = 5,
) -> Sequence[BookOffer]:
    book_repo = BookRepository(session)
    total_count, result = await book_repo.get_all(limit=size, offset=(page - 1) * size)
    response.headers["X-Total-Count"] = str(total_count)
    return result


@router.get("/{bookId}")
async def get_book_offer_by_id(
    session: SessionDependency,
    book_id: Annotated[int, Path(alias="bookId")],
) -> BookOffer:
    book_repo = BookRepository(session)
    try:
        result = await book_repo.get(id=book_id)
    except NotFoundError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Book offer not found",
        ) from e

    return result


@router.post("")
async def add_book_offer(
    book_create: Annotated[BookOfferCreate | str, Form()],
    file: Annotated[UploadFile, File()],
    session: SessionDependency,
) -> BookOffer:
    try:
        book_create_dict = json.loads(book_create)
        book_create_data = BookOfferCreate(**book_create_dict)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Некорректный JSON в поле 'book_create'",
        ) from e
    except ValidationError as e:
        raise RequestValidationError([e.errors()]) from e

    book_repo = BookRepository(session)
    point_repo = PointRepository(session)
    book_image_repo = BookMainImageRepository(session)

    point_db = await point_repo.get(id=book_create_data.point_id)
    if not point_db:
        msg = "Point not found"
        raise HTTPException(detail=msg, status_code=status.HTTP_404_NOT_FOUND)

    filename = await save_uploaded_file(file)
    path = get_file_url(filename)
    main_image = await book_image_repo.create(url=path)
    result = await book_repo.create(
        main_image_id=main_image.id,
        is_active=True,
        **book_create_data.model_dump(exclude={"main_photo_url"}),
    )
    result.main_photo_url = path
    return result


@router.patch("/{bookId}")
async def update_book_offer(
    book_update: BookOfferUpdate,
    session: SessionDependency,
    book_id: Annotated[int, Query(alias="bookId")],
) -> BookOffer:
    repository_manager = RepositoryManager(session)
    service = BookOfferService(repository_manager, repository_manager.book_offer_repo)
    try:
        result = await service.update(book_id, book_update)
    except NotFoundError as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    await session.commit()
    return result
