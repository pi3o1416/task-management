
from django.db.models import Model
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView


class TemplateAPIView(APIView):
    def get_object(self, pk):
        assert hasattr(self, 'model'), "Define a model attribute on your class"
        assert type(self.model) is type(Model), "model should be inherited from ModelBase"
        obj = self.model.objects.get_object_by_pk(pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj


class TemplateViewSet(ViewSet):
    def get_object(self, pk):
        assert hasattr(self, 'model'), "Define a model attribute on your class"
        assert type(self.model) is type(Model), "model should be inherited from ModelBase"
        obj = self.model.objects.get_object_by_pk(pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj






