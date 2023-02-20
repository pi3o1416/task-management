
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView


class TemplateAPIView(APIView):
    def __init__(self, model=None, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def get_object(self, pk):
        assert self.model != None, "Initialize model before get object"
        obj = self.model.objects.get_object_by_pk(pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj


class TemplateViewSet(ViewSet):
    def __init__(self, model=None, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def get_object(self, pk):
        assert self.model != None, "Initialize model before get object"
        obj = self.model.objects.get_object_by_pk(pk=pk)
        self.check_object_permissions(self.request, obj=obj)
        return obj






