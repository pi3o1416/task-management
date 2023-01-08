
from functools import reduce
from operator import __and__
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import UserManager
from django.db.models import Q
from rest_framework.exceptions import NotFound


class CustomUserManager(UserManager):
    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)

    def active_users(self):
        return self.get_queryset().active_users()

    def inactive_users(self):
        return self.get_queryset().inactive_users()

    def staff_users(self):
        return self.get_queryset().staff_users()

    def get_user(self, **kwargs):
        return self.get_queryset().get_user(**kwargs)

    def get_user_by_encoded_pk(self, encoded_pk):
        return self.get_queryset().get_user_by_encoded_pk(encoded_pk=encoded_pk)


class CustomUserQuerySet(QuerySet):
    def active_users(self):
        return self.filter(Q(is_active=True))

    def inactive_users(self):
        return self.filter(Q(is_active=False))

    def staff_users(self):
        return self.filter(Q(is_staff=True))

    def get_user(self, **kwargs):
        try:
            q_objects = [Q(**{key: value}) for key, value in kwargs.items()]
            return self.filter(reduce(__and__, q_objects)).first()
        except:
            return None

    def get_user_by_encoded_pk(self, encoded_pk):
        try:
            pk_bytes = urlsafe_base64_decode(encoded_pk)
            pk = int(pk_bytes)
            user = self.get(pk=pk)
            return user
        except ObjectDoesNotExist:
            raise NotFound({"detail": [_("Invalid uid")]})













