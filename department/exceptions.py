
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class RestrictedDeletionError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Instance deletion restricted due to foreign key restriction')
    default_code = 'restricted'


class DepartmentGetException(Exception):
    pass


class DesignationGetException(Exception):
    pass


class DepartmentMemberGetException(Exception):
    pass










