
from rest_framework import serializers
from .auth_serializers import *
from .basic_serializers import *



class MessageSerializer(serializers.Serializer):
    """
    Only used for documentations
    """
    detail = serializers.ListField()

class ErrorResponse(serializers.Serializer):
    detail = serializers.ListField()
    field_errors = serializers.JSONField()


class ResponseSerializer(serializers.Serializer):
    status=serializers.IntegerField()
    data=serializers.JSONField()
    error=ErrorResponse()



