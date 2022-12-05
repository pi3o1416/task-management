
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager

from .querysets import CustomUserQuerySet

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


