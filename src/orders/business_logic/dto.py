from dataclasses import dataclass


@dataclass
class OrderDTO:
    """
    Data transfer object for storing and transferring data to add
    a new order instance.
    """

    customer_id: int
    robot_serial: str
