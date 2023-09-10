from django.core.mail import send_mail

from train_station_api import settings


def send_email_notifications(
        subject: str, recipient: tuple, message: str
) -> None:
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient,
        fail_silently=False,
    )
