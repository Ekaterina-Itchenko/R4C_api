from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import TYPE_CHECKING
from urllib.parse import quote

from dacite.exceptions import MissingValueError, WrongTypeError
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pandas import DataFrame, ExcelWriter

from common.converters import convert_data_from_request_to_dto
from robots.business_logic.dto import AddRobotDTO
from robots.business_logic.services import create_robot, get_robots
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
    To create a robot.

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


@csrf_exempt
@require_http_methods(request_method_list=["GET"])
def load_robots_info_controller(request: HttpRequest) -> HttpResponse:
    """
    To save excel file with information of robots production and return
    a link to download this file.
    """

    versions = get_robots()
    summary_data: dict[str, dict[str, int]] = {}

    for version in versions:
        model_name = version["model__name"]
        model_version = version["version"]
        robots_count = version["robots_count"]

        summary_data.setdefault(model_name, {})[model_version] = robots_count

    absolute_path = os.path.dirname(os.path.dirname(__file__))
    if not os.path.exists(os.path.join(absolute_path, "data")):
        os.makedirs(os.path.join(absolute_path, "data"))

    file_path = os.path.join(absolute_path, "data", "robot_summary.xlsx")

    with ExcelWriter(file_path, engine="openpyxl") as writer:
        for model_name in summary_data:
            data = []
            for model_version, robots_count in summary_data[model_name].items():
                data.append([model_name, model_version, robots_count])
            df = DataFrame(data, columns=["Модель", "Версия", "Количество"])
            df.to_excel(writer, sheet_name=model_name, index=False)

    full_path = reverse("download_robots_info_file", kwargs={"file_path": quote(file_path)})
    path = f"http://{settings.DOMAIN}{full_path}"
    link = json.dumps({"file_path": path})
    return HttpResponse(content=link)


@require_http_methods(request_method_list=["GET"])
def download_view(request: HttpRequest, file_path: str) -> HttpResponse:
    file_path = quote(file_path)

    with open(file_path, "rb") as file:
        response = HttpResponse(file.read())
        response["Content-Disposition"] = f'attachment; filename="{file_path}"'
        return response
