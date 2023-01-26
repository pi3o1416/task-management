
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..permissions import IsAssignedUponUser
from ..serializers import SubTaskCreateSerializer, TaskTreeDetailSerializer, TaskSerializer
from ..models import Task


class CreateSubTask(APIView):
    serializer_class = SubTaskCreateSerializer
    permission_classes = [IsAuthenticated, IsAssignedUponUser]

    def post(self, request, task_pk):
        user = request.user
        parent_task = self.get_object(pk=task_pk)
        self.check_object_permissions(request=request, obj=parent_task)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            child_task = serializer.create(user=user, commit=True)
            task_tree = serializer.create_task_tree(child=child_task, parent=parent_task, commit=True)
            detail_serializer = TaskTreeDetailSerializer(instance=task_tree)
            return Response(data=detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        task = Task.objects.get_task_by_pk(pk=pk)
        return task


class GetSubTasks(APIView):
    serializer_class = TaskSerializer

    def get(self, request, task_pk):
        task = self.get_object(pk=task_pk)
        subtasks = Task.objects.get_subtasks(parent_task=task)
        serializer = self.serializer_class(instance=subtasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_object(self, pk):
        task = Task.objects.get_task_by_pk(pk=pk)
        return task






