import datetime as dt

from sqlalchemy import MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import settings


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        nullable=True, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        nullable=True, onupdate=lambda: dt.datetime.now(dt.UTC)
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.id})>"


Base.metadata = MetaData(naming_convention=settings.postgres.naming_convention)
