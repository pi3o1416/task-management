
from operator import __and__
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import UserManager
from django.db.models import Q
from rest_framework.exceptions import NotFound
from rest_framework.request import Request

from services.querysets import TemplateQuerySet


class CustomUserManager(UserManager):
    def get_queryset(self):
        return CustomUserQuerySet(self.model, using=self._db)

    def get_object_by_pk(self, pk):
        return self.get_queryset().get_object_by_pk(pk=pk)

    def filter_from_query_params(self, request:Request):
        return self.get_queryset().filter_from_query_params(request=request)

    def get_user_by_encoded_pk(self, encoded_pk):
        return self.get_queryset().get_user_by_encoded_pk(encoded_pk=encoded_pk)



class CustomUserQuerySet(TemplateQuerySet):
    def get_user_by_encoded_pk(self, encoded_pk):
        try:
            pk_bytes = urlsafe_base64_decode(encoded_pk)
            pk = int(pk_bytes)
            user = self.get(pk=pk)
            return user
        except ObjectDoesNotExist:
            raise NotFound({"detail": [_("Invalid uid")]})















