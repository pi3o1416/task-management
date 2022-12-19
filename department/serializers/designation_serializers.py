
from rest_framework import serializers
from ..models import Designations

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designations
        fields = ['pk', 'department', 'title']


class DesignationListSerializer(serializers.Serializer):
    results = DesignationSerializer()
    current_page = serializers.IntegerField()
    total_page = serializers.IntegerField()
    page_limit = serializers.IntegerField()

    def __init__(self, paginator, current_page_no, **kwargs):
        data = self.preprocess_page_data(paginator, current_page_no)
        print(data)
        super().__init__(data=data, **kwargs)

    def preprocess_page_data(self, page, current_page_no):
        data = {
            'results': list(page.get_page(current_page_no)),
            'current_page': current_page_no,
            'total_page': page.num_pages,
            'page_limit': page.per_page
        }
        return data

