
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
