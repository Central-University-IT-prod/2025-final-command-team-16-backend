from pydantic import BaseModel, ConfigDict, Field

from src.utils.partial_schema import partial_schema


class BasePoint(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str = Field(description="City name", min_length=2, max_length=150)
    place: str = Field(description="Place name", min_length=2, max_length=150)


class PointCreate(BasePoint):
    """Schema for point create model."""


@partial_schema
class PointUpdate(BasePoint):
    """Schema for point update model."""


class Point(BasePoint):
    """Schema for point model."""

    id: int = Field(description="Point id", gt=0)
