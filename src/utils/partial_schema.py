from copy import deepcopy
from typing import Any, cast

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


def partial_schema[T: BaseModel](model: type[T]) -> type[T]:
    def make_field_optional(
        field: FieldInfo, default: Any = None
    ) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = field.annotation | None  # type: ignore[assignment, operator]
        return new.annotation, new

    # noinspection PyUnresolvedReferences
    partial_model = create_model(  # type: ignore[call-overload]
        f"Partial{model.__name__}",
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        },
    )
    return cast(type[T], partial_model)
