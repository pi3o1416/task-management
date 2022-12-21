
from .auth_serializers import *
from .basic_serializers import *



class MessageSerializer(serializers.Serializer):
    """
    Only used for documentations
    """
    detail = serializers.ListField()



