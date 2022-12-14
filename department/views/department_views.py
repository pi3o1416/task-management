
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from ..models import Department
from ..serializers import DepartmentSerializer, FieldErrorsSerializer, MessageSerializer
from ..exceptions import DepartmentGetException


class DepartmentViewSet(ViewSet):
    @extend_schema(request=DepartmentSerializer, responses={201: DepartmentSerializer,
                                                            400: FieldErrorsSerializer})
    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={200: DepartmentSerializer})
    def list(self, request):
        print(request.data)
        serializer_class = self.get_serializer_class()
        departments = Department.objects.all()
        serializer = serializer_class(instance=departments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=DepartmentSerializer, responses={202: DepartmentSerializer,
                                                            400: FieldErrorsSerializer,
                                                            404: MessageSerializer})
    def update(self, request, pk):
        try:
            department = Department.objects.get(pk=pk)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=department, data=request.data)
            if serializer.is_valid():
                serializer.update()
                return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DepartmentGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(responses={200: MessageSerializer,
                              404: MessageSerializer})
    def destroy(self, request, pk):
        try:
            department = Department.objects.get_department(pk=pk)
            department.delete()
            return Response(data={"detail": ("Department delete successful",)}, status=status.HTTP_200_OK)
        except DepartmentGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(responses={200: DepartmentSerializer,
                              404: MessageSerializer})
    def retrieve(self, request, pk):
        try:
            serializer_class = self.get_serializer_class()
            department = Department.objects.get_department(pk=pk)
            serializer = serializer_class(instance=department)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except DepartmentGetException as exception:
            return Response(data={"detail": exception.args}, status=status.HTTP_404_NOT_FOUND)

    def get_serializer_class(self):
        return DepartmentSerializer














