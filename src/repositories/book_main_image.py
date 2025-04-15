from typing import Any

from sqlalchemy import update

from src.core.exceptions import NotFoundError
from src.models.book_main_image import BookMainImage
from src.repositories.base.base import BaseDBRepositoryWithModel


class BookMainImageRepository(BaseDBRepositoryWithModel[BookMainImage]):
    model = BookMainImage

    async def create(self, **fields: Any) -> BookMainImage:
        book_main_image = BookMainImage(**fields)
        self.session.add(book_main_image)
        await self.session.commit()
        return book_main_image

    async def update(self, book_main_image_id: int, **fields: Any) -> BookMainImage:
        query = await self.session.scalars(
            update(BookMainImage)
            .where(BookMainImage.id == book_main_image_id)
            .values(**fields)
            .returning(BookMainImage),
        )
        result = query.first()
        if not result:
            raise NotFoundError
        await self.session.commit()
        return result
