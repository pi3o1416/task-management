
from functools import reduce
from operator import __and__
from django.utils.http import urlsafe_base64_decode
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


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
            return None













