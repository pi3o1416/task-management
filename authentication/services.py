
from django.urls import reverse_lazy
from django.conf import settings

def get_absolute_uri(request, url_name, **kwargs):
    url = reverse_lazy(url_name, kwargs=kwargs)
    absolute_uri = request.build_absolute_uri(url)
    return absolute_uri


