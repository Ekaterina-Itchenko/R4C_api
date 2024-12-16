from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db.models import Count
from django.utils import timezone

from common.utils import query_debugger
from robots.business_logic.dto import AddRobotDTO
from robots.business_logic.services.errors import (
    RobotModelDoesNotExistError,
    RobotVersionDoesNotExistError,
)
from robots.models import Robot, RobotModel, RobotVersion

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


@query_debugger
def create_robot(data: AddRobotDTO) -> None:
    """
    Create a new robot.
    Args:
        data (AddRobotDTO): Data containing robot information.
    Returns:
        None
    """

    try:
        model = RobotModel.objects.get(name=data.model)
        version = RobotVersion.objects.get(version=data.version, model=model.pk)

        robot = Robot.objects.create(
            version=version,
            created=data.created,
            serial=data.model + "-" + data.version,
        )
        logger.info(msg="A robot instance has been created", extra={"model": robot.serial})
    except RobotModel.DoesNotExist:
        logger.error(msg="A model does not exist.", extra={"model": data.model})
        raise RobotModelDoesNotExistError(f"Model [{data.model}] does not exist.")

    except RobotVersion.DoesNotExist:
        logger.error(
            msg="A model version does not exist.",
            extra={"model": data.model, "version": data.version},
        )
        raise RobotVersionDoesNotExistError(f"There is no version [{data.version}] for robots models.")


@query_debugger
def get_robots(days: int = 7) -> QuerySet:
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=days)

    versions = (
        RobotVersion.objects.annotate(robots_count=Count("robots", distinct=True))
        .select_related("model")
        .prefetch_related("robots")
        .filter(robots__created__range=(start_date, end_date))
        .values("model__name", "version", "robots_count")
        .order_by("model__name")
    )
    return versions.all()


@query_debugger
def get_robots_by_serial(serial: str, is_active: bool) -> QuerySet[Robot]:
    result = Robot.objects.filter(serial=serial, is_active=is_active).all()
    return result
