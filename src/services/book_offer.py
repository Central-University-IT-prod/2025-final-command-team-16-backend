from src.core.exceptions import NotFoundError
from src.repositories import BookRepository
from src.schemas import BookOffer, BookOfferCreate, BookOfferUpdate
from src.services.base import BaseDBService


class BookOfferService(BaseDBService[BookOffer, BookRepository]):
    async def create(self, book_create: BookOfferCreate) -> BookOffer:
        point = await self.repository_manager.point_repo.get(id=book_create.point_id)
        if not point:
            msg = "Point not found"
            raise NotFoundError(msg)
        result = await self.repository.create(**book_create.model_dump())
        if result is None:
            msg = "Book not found"
            raise NotFoundError(msg)
        return result

    async def update(self, book_id: int, book_update: BookOfferUpdate) -> BookOffer:
        if book_update.point_id is not None:
            point = await self.repository_manager.point_repo.get(
                id=book_update.point_id,
            )
            if not point:
                msg = "Point not found"
                raise NotFoundError(msg)
        result = await self.repository.update(
            book_id=book_id, **book_update.model_dump()
        )
        if result is None:
            raise NotFoundError
        return result
