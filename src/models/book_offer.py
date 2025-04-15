from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.book_main_image import BookMainImage
    from src.models.point import Point


class BookOffer(Base):
    __tablename__ = "book_offers"

    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(50))
    genre: Mapped[str | None] = mapped_column(String(100))
    year: Mapped[int]
    publisher: Mapped[str | None]
    language: Mapped[str | None] = mapped_column(String(30))
    binding: Mapped[str | None]
    pages_count: Mapped[int | None]
    size: Mapped[str | None]
    condition: Mapped[str | None]
    description: Mapped[str | None] = mapped_column(String(1000))
    is_active: Mapped[bool]
    point_id: Mapped[int] = mapped_column(
        ForeignKey("points.id", ondelete="SET NULL"),
    )
    main_image_id: Mapped[int] = mapped_column(
        ForeignKey("book_main_images.id", ondelete="SET NULL"),
        unique=True,
    )

    point: Mapped["Point"] = relationship(back_populates="book_offers")
    main_photo: Mapped["BookMainImage"] = relationship(back_populates="book_offer")
