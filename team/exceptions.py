
from rest_framework import status
from rest_framework.exceptions import APIException


class MemberBulkAddFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bulk_team_member_add_failed'
    default_detail = 'Bulk member add failed'


class MemberBulkRemoveFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'bulk_team_member_remove_failed'
    default_detail = 'Bulk member delete failed'


class TeamLeadDeleteProhabited(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'team_lead_delete_prohabited'
    default_detail = 'Team lead can not be deleted'


class TeamCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'team_create_failed'
    default_detail = 'Team create failed'


class TeamTaskCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'team_task_create_failed'
    default_detail = 'Team task create failed'


class TeamTaskDeleteFailed(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'team_task_delete_failed'
    default_detail = 'Team task delete failed'


class TeamInternalTaskCreateFailed(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'team_internal_task_create_failed'
    default_detail = 'Team internal task create failed'




