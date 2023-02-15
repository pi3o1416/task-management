
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from ..serializers import ProjectMemberSerializer, ProjectMemberBulkCreateSerializer
from ..models import Project

User = get_user_model()


class APIViewTemplate(APIView):
    def __init__(self, model=None):
        self.model = model

    def get_object(self, pk):
        assert self.model != None, "Initialize model before get object"
        return self.model.objects.get_object_by_pk(pk)


class ProjectMemberCreateView(APIViewTemplate):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectMemberBulkCreateSerializer

    def __init__(self):
        super().__init__(model=Project)

    def post(self, request, project_pk):
        project = self.get_object(pk=project_pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            project_members = serializer.create(project=project, commit=True)
            response_serializer = ProjectMemberSerializer(instance=project_members, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectMemberDeleteView(APIViewTemplate):
    def __init__(self):
        super().__init__(model=Project)

    def delete(self, request, project_pk, user_pk):
        project = self.get_object(pk=project_pk)
        project_member = User.objects.get_user_by_pk(pk=user_pk)
        project.delete_project_member(project_member)
        return Response(data={"detail": _("Project member delete successful")})


class MembersOfProjectView(APIViewTemplate, PageNumberPagination):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__(model=Project)

    def get(self, request, project_pk):
        project = self.get_object(pk=project_pk)
        serializer_fields = tuple(self.serializer_class().fields)
        project_members = project.members.all().values(*serializer_fields)
        page = self.paginate_queryset(queryset=project_members, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)










