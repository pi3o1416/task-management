
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task(name='add_two_number')
def add(x, y):
    raise Exception


@shared_task(name='send_email')
def send_email(subject, email_to, message):
    email_from = settings.EMAIL_HOST_USER
    email = EmailMessage(
        subject=subject,
        from_email=email_from,
        to=email_to,
        body=message
    )
    email.send()





