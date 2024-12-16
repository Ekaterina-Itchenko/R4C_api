from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from common.send_email import send_email_to_user
from orders.business_logic.orders import get_pending_orders_by_serial
from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Robot)
def send_notifications_to_user(sender: Robot, instance: Robot, created: bool, **kwargs: Any) -> None:
    if created:
        pending_orders = get_pending_orders_by_serial(serial=instance.serial)
        if pending_orders:
            order: Order = pending_orders[0]
            text = (
                f"Добрый день!"
                f"Недавно Вы интересовались нашим роботом модели"
                f"{instance.version.model.name}, версии {instance.version.version}."
                f"Этот робот теперь в наличии. Если вам подходит этот вариант -"
                f"пожалуйста, свяжитесь с нами"
            )
            send_email_to_user(subject="The robot is in stock.", user=order.customer, email_text=text)
