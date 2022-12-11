
from django.urls import reverse_lazy
from django.conf import settings

def get_absolute_uri(url_name, **kwargs):
    url = reverse_lazy(url_name, kwargs=kwargs)
    absolute_uri = settings.DOMAIN_URI + url
    return absolute_uri


