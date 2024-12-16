import logging

from django.core.mail import send_mail

from customers.models import Customer

logger = logging.getLogger(__name__)


def send_email_to_user(user: Customer, email_text: str, subject: str) -> None:
    """
    Send email to customer.
    """

    send_mail(
        subject=subject,
        message=email_text,
        from_email=user.email,
        recipient_list=[user.email],
    )
    logger.info(msg="Message of a robot creation has sent", extra={"user": user.pk})
    return None
