
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(UserManager):
    pass


class CustomUser(AbstractUser):
    email = models.EmailField(
        _("email address"),
        blank=False,
        unique=True,
        null=False)

    objects = CustomUserManager()

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


