
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from ..permissions import CanViewAllTasks
from ..serializers import TaskSerializer
from ..models import Task


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

    def list(self, request):
        tasks = Task.objects.filter_from_query_params(request)
        page = self.paginate_queryset(queryset=tasks, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)


    def get_serializer_class(self):
        return TaskSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes += []
        if self.action == 'list':
            permission_classes += [CanViewAllTasks]
        return [permission() for permission in permission_classes]






