
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class TaskCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Task create failed")
    default_code = 'task_create_failed'


class UserTasksCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("User task create failed")
    default_code = 'user_task_create_failed'


class UserTasksDeleteFailed(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'user_task_delete_failed'
    default_detail = _("User task delete failed")


class TaskAttachmentCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Task attachment create failed")
    default_code = 'user_task_create_failed'


class TaskTreeCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Task tree create failed")
    default_code = 'task_tree_create_failed'


class TaskDeleteRestricted(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("Task can not be deleted once it has already been assigned or started")
    default_code = 'task_delete_restricted'


