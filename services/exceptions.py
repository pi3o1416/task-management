
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status


class DBOperationFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Database operation failed")
    default_code = 'db_operation_failed'


class InvalidRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invalid request, does not match with current state")
    default_code = 'invalid_request'


class TableEntityDeleteRestricted(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Database table entity delete restricted")
    default_code = 'entity_delete_restricted'


class InvalidDataType(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _("Invalid datatype")
    default_code = 'invalid_datatype'


class InvalidFieldName(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = _("Invalid field name passed for update")
    default_code = 'invalid_field_name'


class UpdateProhabitedField(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = _("Field is restricted for any update")
    default_code = 'update_prohabited_field'




