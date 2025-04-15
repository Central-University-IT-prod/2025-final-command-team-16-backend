from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select, update
from sqlalchemy.orm import aliased, joinedload

from src.core.exceptions import NotFoundError
from src.models import BookMainImage, BookOffer, Point
from src.repositories.base import BaseDBRepositoryWithModel


class BookRepository(BaseDBRepositoryWithModel[BookOffer]):
    model = BookOffer

    async def get(self, **filters: Any):
        query = await self.session.scalars(
            select(BookOffer)
            .options(joinedload(BookOffer.main_photo))
            .options(joinedload(BookOffer.point))
            .filter_by(**filters)
        )
        book_offer = query.first()
        print(book_offer.point)
        if book_offer:
            book_offer.main_photo_url = (
                book_offer.main_photo.url if book_offer.main_photo else None
            )
            delattr(book_offer, "main_photo")
            book_offer.point_city = book_offer.point.city
            book_offer.point_place = book_offer.point.place
            delattr(book_offer, "point")

        return book_offer

    async def get_all(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters: Any,
    ) -> tuple[int, Sequence[dict]]:
        main_photo_alias = aliased(BookMainImage, name="main_photo_alias")

        stmt = (
            select(
                BookOffer,
                Point,
                main_photo_alias.url.label("main_photo_url"),
            )
            .join(
                main_photo_alias,
                BookOffer.main_image_id == main_photo_alias.id,
                isouter=True,
            )
            .join(Point, BookOffer.point_id == Point.id, isouter=True)
            .filter_by(**filters)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)

        books = []
        for row in result:
            book_data = row.BookOffer.__dict__  # Преобразуем BookOffer в словарь
            book_data["main_photo_url"] = row.main_photo_url  # Добавляем main_photo_url
            book_data["point_city"] = row.Point.city
            book_data["point_place"] = row.Point.place
            books.append(book_data)

        total_count = await self.session.scalar(
            select(func.count(BookOffer.id)).filter_by(**filters)
        )

        return total_count, books

    async def create(self, **fields: Any) -> BookOffer:
        book = BookOffer(**fields)
        self.session.add(book)
        await self.session.commit()
        return await self.get(id=book.id)

    async def update(self, book_id: int, **fields: Any) -> BookOffer:
        query = await self.session.scalars(
            update(BookOffer)
            .where(BookOffer.id == book_id)
            .values(**fields)
            .returning(BookOffer),
        )
        result = query.first()
        if not result:
            raise NotFoundError
        return result
