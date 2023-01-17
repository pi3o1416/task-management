
from django.contrib.auth.models import Permission, Group
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import PermissionSerializer


class GroupViewSet(ViewSet):
    pass


class PermissionViewSet(ViewSet):
    def list(self, request):
        permissions = Permission.objects.all()
        serializer = self.get_serializer_class()(instance=permissions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return PermissionSerializer

