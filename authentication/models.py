
import os
from django.template.loader import render_to_string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from emailservice.emailclient import send_async_email

from services.mixins import ModelUpdateMixin, ModelDeleteMixin
from .validators import validate_aamarpay_email
from .querysets import CustomUserManager
from .services import get_absolute_uri, ACTIVE_ACCOUNT_EMAIL_SUBJECT, PASSWORD_RESET_EMIAL_SUBJECT


def user_photo_upload_path(instance, file):
    _, file_extension = os.path.splitext(file)
    file_path = 'users-photos/{}/profile_picture{}'.format(instance.username, file_extension)
    return file_path


class CustomUser(ModelUpdateMixin, ModelDeleteMixin, AbstractUser):
    restricted_fields = ['pk']
    error_messages = {
        "CREATE": "User create failed.",
        "UPDATE": "User update failed.",
        "DELETE": "User delete failed.",
        "RETRIEVE": "User retrieve failed.",
        "PATCH": "User patch failed.",
    }

    photo = models.ImageField(
        verbose_name=_("User photo"),
        upload_to=user_photo_upload_path,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        null=False,
        validators=[validate_aamarpay_email]
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    objects = CustomUserManager()

    class Meta:
        ordering = ['username']

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

    def send_password_reset_email(self):
        token = self.generate_token()
        uidb64 = self.generate_urlsafe_b64_encoded_pk()
        absolute_uri = get_absolute_uri('authentication:reset-password', uidb64=uidb64, token=token)
        subject = PASSWORD_RESET_EMIAL_SUBJECT
        email_to = [self.email]
        context = {
            'full_name': self.full_name,
            'absolute_uri': absolute_uri
        }
        html_message = render_to_string('password-reset-email.html', context=context)
        send_async_email(subject=subject, email_to=email_to, message=html_message)
        return True


    def send_account_active_email(self):
        token = self.generate_token()
        uidb64 = self.generate_urlsafe_b64_encoded_pk()
        absolute_uri = get_absolute_uri('authentication:active-account', uidb64=uidb64, token=token)
        subject = ACTIVE_ACCOUNT_EMAIL_SUBJECT
        email_to = [self.email]
        context = {
            'full_name': self.full_name,
            'absolute_uri': absolute_uri
        }
        html_message = render_to_string('account-active-email.html', context=context)
        send_async_email(subject=subject, email_to=email_to, message=html_message)

    def activate_account(self):
        if self.is_active != True:
            self.update(is_active=True)
        return True

    def inactivate_account(self):
        if self.is_active != False:
            self.update(is_active=False)
        return True

    def give_staff_permissions(self):
        if self.is_staff != True:
            self.update(is_active=True)
        return True

    def remove_staff_permissions(self):
        if self.is_staff != False:
            self.update(is_active=False)
        return True













