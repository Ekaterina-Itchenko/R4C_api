import logging
from typing import Any, TypeVar

from dacite import from_dict
from dacite.exceptions import MissingValueError, WrongTypeError

from common.errors import InvalidNumberParametersError, WrongParameterTypeError

T = TypeVar("T")

logger = logging.getLogger(__name__)


def convert_data_from_request_to_dto(dto: type[T], data_from_request: dict[str, Any]) -> T:
    """The function converts the data into a data transfer object."""
    try:
        result: T = from_dict(dto, data_from_request)
        return result
    except MissingValueError:
        logger.error(msg="Invalid number of parameters.", extra={"data": data_from_request})
        raise InvalidNumberParametersError("Invalid number of parameters to create a robot instance.")
    except WrongTypeError:
        logger.error(msg="Invalid type of parameters.", extra={"data": data_from_request})
        raise WrongParameterTypeError("Invalid type of parameters.")
