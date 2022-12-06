
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager

from .querysets import CustomUserQuerySet
from .services import get_absolute_uri

CustomUserManager = UserManager.from_queryset(CustomUserQuerySet)


class CustomUser(AbstractUser):
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        null=False)

    objects = CustomUserManager()

    class Meta:
        ordering = ['username']
        pass

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def generate_urlsafe_b64_encoded_pk(self):
        pk_str = str(self.pk)
        pk_bytes = bytes(pk_str, 'utf-8')
        encoded_pk = urlsafe_base64_encode(pk_bytes)
        return encoded_pk

    def generate_token(self):
        token = default_token_generator.make_token(user=self)
        return token

    def validate_token(self, token):
        return default_token_generator.check_token(user=self, token=token)

    def send_password_reset_email(self, request):
        token = self.generate_token()
        uidb64 = self.generate_urlsafe_b64_encoded_pk()
        absolute_uri = get_absolute_uri(request, 'authentication:reset-password', uidb64=uidb64, token=token)
        subject = 'Reset Password'
        email_from = settings.EMAIL_HOST_USER
        email_to = [self.email]
        context = {
            'full_name': self.full_name,
            'absolute_uri': absolute_uri
        }
        html_message = render_to_string('password-reset-email.html', context=context)
        self.send_email(subject, email_from, email_to, message=html_message)


    def send_account_active_email(self):
        token = self.generate_token()
        uidb64 = self.generate_urlsafe_b64_encoded_pk()
        url = reverse_lazy()

    def send_email(self, subject, email_from, email_to, message=""):
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=email_from,
            to=email_to
        )
        email.send()










