from pydantic import BaseModel, ConfigDict, Field

from src.enums import BookBindingType, BookGenreType, BookSizeType, BookStateType
from src.utils.partial_schema import partial_schema


class BaseBookOffer(BaseModel):
    model_config = ConfigDict(use_enum_values=True, from_attributes=True)

    name: str = Field(description="Book name", min_length=3, max_length=100)
    author: str = Field(description="Author name", min_length=3, max_length=50)
    year: int = Field(ge=0, le=3000, description="Book publication year")
    genre: BookGenreType | None = Field(description="Book genre")
    publisher: str | None
    language: str | None = Field(
        description="Book language",
        min_length=3,
        max_length=30,
    )
    binding: BookBindingType | None = Field(description="Book binding type")
    pages_count: int | None = Field(description="Book pages number", ge=1, le=10000)
    size: BookSizeType | None = Field(description="Book size")
    condition: BookStateType | None = Field(description="Book physical state")
    description: str | None = Field(description="Book description", max_length=1000)
    point_id: int = Field(description="Point id", gt=0)


class BookOffer(BaseBookOffer):
    """Book offer schema."""

    id: int = Field(description="Book offer id", gt=0)
    main_photo_url: str = Field(
        description="Main book photo url",
        min_length=3,
        max_length=250,
    )
    point_city: str
    point_place: str


class BookOfferCreate(BaseBookOffer):
    """Book offer create schema."""


@partial_schema
class BookOfferUpdate(BaseBookOffer):
    """Book offer update schema."""
