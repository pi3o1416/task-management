
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from services.pagination import CustomPageNumberPagination
from services.views import TemplateViewSet

from ..documentations import department_docs as docs
from ..models import Department
from ..serializers import DepartmentSerializer


class DepartmentViewSet(TemplateViewSet, CustomPageNumberPagination):
    model = Department
    permission_classes = [DjangoModelPermissions]
    queryset = Department.objects.all()

    @extend_schema(
        responses=docs.DepartmentViewSetCreateDoc.responses,
        parameters=docs.DepartmentViewSetCreateDoc.parameters
    )
    def create(self, request):
        """
        Create New Department
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=docs.DepartmentViewSetListDoc.responses,
        parameters=docs.DepartmentViewSetListDoc.parameters
    )
    def list(self, request):
        """
        List of all Department
        """
        serializer_class = self.get_serializer_class()
        departments = Department.objects.all()
        page = self.paginate_queryset(queryset=departments, request=request)
        serializer = serializer_class(instance=page, many=True)
        return self.get_paginated_response(data=serializer.data)

    @extend_schema(
        responses=docs.DepartmentViewSetUpdateDoc.responses,
        parameters=docs.DepartmentViewSetUpdateDoc.parameters
    )
    def update(self, request, pk):
        """
        Update department
        URL parameter: Department Primary key(pk)
        """
        department = self.get_object(pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=department, data=request.data)
        if serializer.is_valid():
            serializer.update()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=docs.DepartmentViewSetDestroyDoc.responses,
        parameters=docs.DepartmentViewSetDestroyDoc.parameters
    )
    def destroy(self, request, pk):
        """
        Destroy Department
        URL Parameter: Department Primary Key(pk)
        """
        department = self.get_object(pk=pk)
        department.delete()
        return Response(data={"detail": ("Department delete successful",)}, status=status.HTTP_200_OK)

    @extend_schema(
        responses=docs.DepartmentViewSetRetrieveDoc.responses,
        parameters=docs.DepartmentViewSetRetrieveDoc.parameters
    )
    def retrieve(self, request, pk):
        """
        Retrieve Department
        URL Parameter: Department Primary Key(Pk)
        """
        serializer_class = self.get_serializer_class()
        department = self.get_object(pk=pk)
        serializer = serializer_class(instance=department)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return DepartmentSerializer














