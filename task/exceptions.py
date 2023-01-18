
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class DBOperationFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Database operation failed")
    default_code = 'db_operation_failed'

