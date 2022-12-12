
from .tasks import add, send_email


def send_async_email(subject, email_to, message):
    return send_email.delay(subject, email_to, message)













