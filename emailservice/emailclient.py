
from .tasks import add, send_email
from tms.celery import app


def send_async_email(subject, email_to, message):
    temp = {
        "subject": subject,
        "email_to": email_to,
        "message": message
    }
    app.send_task("send_email", kwargs=temp)
    return True













