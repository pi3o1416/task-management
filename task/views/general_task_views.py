
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from ..serializers import TaskSerializer


class TaskViewSet(ViewSet, PageNumberPagination):
    def create(self, request):
        user = request.user
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            task = serializer.create(commit=False)
            task.update_task_owner(user, commit=False)
            task.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer_class(self):
        return TaskSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes += []
        return [permission() for permission in permission_classes]






