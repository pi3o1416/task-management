
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


class InvalidFieldName(APIException):
    def __init__(self, model_name:str="", field_name:str="", *args, **kwargs):
        if model_name and field_name:
            self.default_detail = _("{} is an invalid field of {} table"
                                    .format(field_name, model_name))
        super().__init__(*args, **kwargs)

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = _("Invalid field name passed for update")
    default_code = 'invalid_field_name'


class UpdateProhabitedField(APIException):
    def __init__(self, model_name:str="", field_name:str="", *args, **kwargs):
        if model_name and field_name:
            self.default_detail = _("{} field of {} table is prohabited to update"
                                    .format(field_name, model_name))

    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = _("Field is restricted for any update")
    default_code = 'update_prohabited_field'


class TableEntityDeleteRestricted(APIException):
    def __init__(self, model_name=None, *args, **kwargs):
        breakpoint()
        if model_name != None:
            self.default_detail = _("{} table entity delete restricted".format(model_name))
        super().__init__(*args, **kwargs)

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Database table entity delete restricted")
    default_code = 'entity_delete_restricted'


class InvalidDataType(APIException):
    def __init__(self, expected_dtype:type, find_dtype:type, model_name=None, *args, **kwargs):
        model_name = "" if model_name == None else model_name
        self.default_detail = _("Invalid data type on {} object retrieve. Expected {} but got {}"
                                .format(model_name, expected_dtype.__name__, find_dtype.__name__))
        super().__init__(*args, **kwargs)

    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = _("Invalid datatype")
    default_code = 'invalid_datatype'


class ObjectNotFound(APIException):
    def __init__(self, model_name, *args, **kwargs):
        self.default_detail = _("{} object does not exist".format(model_name))
        super().__init__(*args, **kwargs)

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = _("Object does not exist")
    default_code = 'does_not_exist'




