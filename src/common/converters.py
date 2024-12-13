from typing import Any, TypeVar

from dacite import from_dict

T = TypeVar("T")


def convert_data_from_request_to_dto(dto: type[T], data_from_request: dict[str, Any]) -> T:
    """The function converts the data into a data transfer object."""

    result: T = from_dict(dto, data_from_request)
    return result
