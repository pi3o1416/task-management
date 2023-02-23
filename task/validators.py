
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_task_submission_last_date(last_date):
    current_time = timezone.now()
    if last_date <= current_time:
        raise ValidationError(_("Task last date should be greater than current time"))
    return last_date
