from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.book_offer import BookOffer


class BookMainImage(Base):
    __tablename__ = "book_main_images"

    url: Mapped[str] = mapped_column(String(250))

    book_offer: Mapped["BookOffer"] = relationship(back_populates="main_photo")
