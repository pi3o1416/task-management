
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





