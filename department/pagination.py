
from rest_framework.pagination import PageNumberPagination

class SmallPageNumberPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'


class MediumPageNumberPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'


class LargePageNumberPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'











