
from .department_member_serializers import *
from .department_serializers import *
from .designation_serializers import *
from rest_framework import serializers

class FieldErrorsSerializer(serializers.Serializer):
    """
    Only use for documentation
    """
    field_name = serializers.ListField()


class MessageSerializer(serializers.Serializer):
    """
    Only use for documentation
    """
    detail = serializers.ListField()

