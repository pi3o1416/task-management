
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from department.models import Department
from ..serializers import ProjectSerializer, ProjectDetailSerializer
from ..models import Project


class ProjectViewSet(ViewSet, PageNumberPagination):
    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            project = serializer.create(validated_data=serializer.validated_data)
            response_serializer = ProjectDetailSerializer(instance=project)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        projects = self.get_queryset(request)
        page = self.paginate_queryset(queryset=projects, request=request)
        serializer = self.get_serializer_class()(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def retrieve(self, request, pk):
        project = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(instance=project)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        #TODO: Fix Broken pipe from 127.0.0.1 51792 on 204 response
        project = self.get_object(pk=pk)
        project.delete()
        return Response(data={"detail": _("Project delete successful")}, status=status.HTTP_202_ACCEPTED)

    def update(self, request, pk):
        project = self.get_object(pk=pk)
        serializer = self.get_serializer_class()(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.update()
            response_serializer = ProjectDetailSerializer(instance=project)
            return Response(data=response_serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=True, url_path='start-project')
    def active_project(self, request, pk):
        project = self.get_object(pk)
        project.active_project()
        response_serializer = ProjectDetailSerializer(instance=project)
        return Response(data=response_serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='pause-project')
    def pause_project(self, request, pk):
        project = self.get_object(pk)
        project.pause_project()
        response_serializer = ProjectDetailSerializer(instance=project)
        return Response(data=response_serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(methods=['patch'], detail=True, url_path='end-project')
    def finish_project(self, request, pk):
        project = self.get_object(pk)
        project.finish_project()
        response_serializer = ProjectDetailSerializer(instance=project)
        return Response(data=response_serializer.data, status=status.HTTP_202_ACCEPTED)

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProjectSerializer
        return ProjectDetailSerializer

    def get_queryset(self, request):
        return Project.objects.filter_with_reverse_related_fields(request)

    def get_object(self, pk):
        return Project.objects.get_object_by_pk(pk=pk)


class DepartmentProjects(APIView, PageNumberPagination):
    serializer_class = ProjectDetailSerializer

    def get(self, request, department_pk):
        department = self.get_object(pk=department_pk)
        department_projects = department.department_projects.all()
        filtered_queryset = department_projects.filter_with_reverse_related_fields(request=request)
        page = self.paginate_queryset(queryset=filtered_queryset, request=request)
        serializer = self.serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    def get_object(self, pk):
        department = Department.objects.get_department(pk)
        return department







