
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ReviewCreateFailed(APIException):
    status_code=status.HTTP_400_BAD_REQUEST
    default_code='review_create_failed'
    default_detail=_('Review create failed')


class GoalCreateFailed(APIException):
    status_code=status.HTTP_400_BAD_REQUEST
    default_code='goal_create_failed'
    default_detail=_("Goal create failed.")


class GoalDeleteFailed(APIException):
    status_code=status.HTTP_202_ACCEPTED
    default_code='goal_delete_failed'
    default_detail=_("Goal delete failed")







