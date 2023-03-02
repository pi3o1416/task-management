
from rest_framework import status
from rest_framework.exceptions import APIException


class DepartmentTaskCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'department_task_create_failed'
    default_detail = 'Department Task Create Failed'
