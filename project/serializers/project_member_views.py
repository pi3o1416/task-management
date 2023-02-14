
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from ..models import ProjectMember


class APIViewTemplate(APIView):
    def __init__(self, model=None):
        self.model = model

    def get_object(self, pk):
        assert self.model != None, "Initialize model before get object"
        return self.model.objects.get_object_by_pk(pk=pk)


class ProjectMemberBulkCreate(APIViewTemplate):
    def post(self, request):
        pass


class ProjectMemberDelete(APIViewTemplate):
    def destroy(self, request, project_member_pk):
        pass


class MembersOfProject(APIViewTemplate):
    def get(self, request, project_pk):
        pass







