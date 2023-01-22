
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from ..permissions import CanViewAllTasks, IsOwner
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

    def destroy(self, request, pk):
        task = Task.objects.get_task_by_pk(pk)
        task.delete()
        return Response(data={"detail": [_("Task delete successful")]}, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, pk):
        task = Task.objects.get_task_by_pk(pk)
        serializer = self.get_serializer_class()(instance=task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        task = Task.objects.get_task_by_pk(pk)
        serializer = self.get_serializer_class()(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.update(instance=task, validated_data=serializer.validated_data)
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return TaskSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'create':
            permission_classes += []
        if self.action == 'list':
            permission_classes += [CanViewAllTasks]
        if self.action == 'retrieve':
            permission_classes += [IsOwner]
        if self.action == 'destroy' or self.action == 'update':
            permission_classes += [IsOwner]

        return [permission() for permission in permission_classes]






