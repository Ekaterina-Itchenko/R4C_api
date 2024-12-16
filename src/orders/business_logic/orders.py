from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from common.utils import query_debugger
from customers.models import Customer
from orders.business_logic.dto import OrderDTO
from orders.business_logic.errors import CustomerDoesNotExistError
from orders.models import Order

if TYPE_CHECKING:
    from django.db.models import QuerySet


logger = logging.getLogger(__name__)


@query_debugger
def create_order(data: OrderDTO) -> Order:
    """
    To create an order.
    """

    try:
        customer = Customer.objects.get(pk=data.customer_id)
        order: Order = Order.objects.create(customer=customer, serial=data.robot_serial)

        logger.info(
            msg="An order instance has been created", extra={"order_id": order.pk, "customer": order.customer.pk}
        )
        return order
    except Customer.DoesNotExist:
        logger.error(msg="Customer does not exist", extra={"customer": order.customer.pk})
        raise CustomerDoesNotExistError(f"Customer [{order.customer.pk}] does not exist.")


@query_debugger
def get_pending_orders_by_serial(serial: str) -> QuerySet[Order]:
    """
    To get pending orders queryset by a robot serial number.
    """

    result = Order.objects.filter(serial=serial, is_waiting=True).order_by("created_at").all()
    return result
