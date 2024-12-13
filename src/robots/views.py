from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import TYPE_CHECKING

from dacite.exceptions import MissingValueError, WrongTypeError
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from common.converters import convert_data_from_request_to_dto
from robots.business_logic.dto import AddRobotDTO
from robots.business_logic.services import create_robot
from robots.business_logic.services.errors import (
    RobotModelDoesNotExistError,
    RobotVersionDoesNotExistError,
)

if TYPE_CHECKING:
    from django.http import HttpRequest


logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(request_method_list=["POST"])
def add_robot_controller(request: HttpRequest) -> HttpResponse:
    """
    Display the home page containing tweets and handling tweet creation.

    Args:
        request: The HTTP request.

    Returns:
        HttpResponse
    """

    data: dict[str, str] = json.loads(request.body)
    created = data.get("created")
    if created:
        try:
            created_datetime_format = datetime.strptime(data["created"], "%Y-%m-%d %H:%M:%S")
            tz = timezone.get_current_timezone()
            cteated_date = timezone.make_aware(value=created_datetime_format, timezone=tz)
            data["created"] = cteated_date
        except ValueError:
            logger.error(msg="Invalid date format.", extra={"created_at": data["created"]})
            return HttpResponseBadRequest(content="Invalid date format. Correct date format - YYYY-MM-DD HH:MM:SS")
    else:
        logger.error(msg="There is no created parameter.")
        return HttpResponseBadRequest("Created parameter is required.")

    try:
        robot_dto = convert_data_from_request_to_dto(dto=AddRobotDTO, data_from_request=data)
        create_robot(data=robot_dto)
        return HttpResponse(status=200)

    except RobotModelDoesNotExistError:
        return HttpResponseBadRequest(content="Model does not exist.")
    except RobotVersionDoesNotExistError:
        return HttpResponseBadRequest(content="Version does not exist.")
    except MissingValueError:
        logger.error(msg="Invalid number of parameters.", extra={"data": data})
        return HttpResponseBadRequest(content="Invalid number of parameters to create a robot instance.")
    except WrongTypeError:
        logger.error(msg="Invalid type of parameters.", extra={"data": data})
        return HttpResponseBadRequest(content="Invalid type of parameters.")
