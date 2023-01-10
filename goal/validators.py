
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def validate_year(year):
    current_year = timezone.now().year
    if current_year-500 <= year <= current_year+500:
        return year
    raise ValidationError("Goal year out of range")


def validate_completion(completion):
    if 0 <= completion <= 100:
        return completion
    raise ValidationError("Goal complete should be range within [0-100]")
