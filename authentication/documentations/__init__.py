
from rest_framework import serializers
from collections import namedtuple


Documentation = namedtuple(
    "Documentation",
    ["request", "responses", "parameters", "examples"],
    defaults=[None, None, None, None]
)


class FieldErrorSerializer(serializers.Serializer):
    field_name = serializers.ListField()


class ErrorResponse(serializers.Serializer):
    detail = serializers.ListField()
    field_errors = FieldErrorSerializer()


class ResponseSerializer(serializers.Serializer):
    status=serializers.IntegerField()
    response_data=serializers.JSONField()
    error=ErrorResponse()
