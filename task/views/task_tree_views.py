
from django.utils.translation import gettext_lazy as _
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..serializers import TaskTreeCreateSerializer, TaskTreeDetailSerializer


class CreateSubtusk(APIView):
    serializer_class = TaskTreeCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            task_tree = serializer.create(user=user)
            detail_serializer = TaskTreeDetailSerializer(instance=task_tree)
            return Response(data=detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)




