
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from ..serializers import UsersTasksSerializers


class UsersTasksViewSet(ViewSet):
    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer_class(self):
        return UsersTasksSerializers

