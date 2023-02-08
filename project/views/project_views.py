
from rest_framework.viewsets import ViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


from ..serializers import ProjectSerializer, ProjectDetailSerializer


class ProjectViewSet(ViewSet, PageNumberPagination):
    def create(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            project = serializer.create(validated_data=serializer.validated_data)
            response_serializer = ProjectDetailSerializer(instance=project)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"field_errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        pass

    def retrieve(self, request, project_pk):
        pass

    def destroy(self, request, project_pk):
        pass

    def update(self, request, project_pk):
        pass

    def get_serializer_class(self):
        return ProjectSerializer
