from dataclasses import dataclass
from datetime import datetime


@dataclass
class AddRobotDTO:
    """
    Data transfer object for storing and transferring data to add
    a new robot instance.
    """

    model: str
    version: str
    created: datetime
