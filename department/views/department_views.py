
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema
from ..models import Department
from ..serializers import DepartmentSerializer, FieldErrorsSerializer


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

    def list(self, request):
        serializer_class = self.get_serializer_class()
        departments = Department.objects.all()
        serializer = serializer_class(instance=departments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

#    def update(self, request, pk):
#        pass
#
#    def destroy(self, request, pk):
#        pass
#
#    def retrieve(self, request, pk):
#        pass
#
    def get_serializer_class(self):
        if self.action == 'create':
            return DepartmentSerializer
        return DepartmentSerializer














