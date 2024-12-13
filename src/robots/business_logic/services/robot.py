import logging

from common.utils import query_debugger
from robots.business_logic.dto import AddRobotDTO
from robots.business_logic.services.errors import (
    RobotModelDoesNotExistError,
    RobotVersionDoesNotExistError,
)
from robots.models import Robot, RobotModel, RobotVersion

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
