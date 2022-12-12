
from .department_member_serializers import *
from .department_serializers import *
from .department_serializers import *
from rest_framework import serializers

class FieldErrorsSerializer(serializers.Serializer):
    """
    Only use for documentation
    """
    field_name = serializers.ListField()
