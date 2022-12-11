
from django.urls import reverse_lazy
from django.conf import settings


ACTIVE_ACCOUNT_EMAIL_SUBJECT = 'Reset Password URL'
PASSWORD_RESET_EMIAL_SUBJECT = 'Account Activation URL'





def get_absolute_uri(url_name, **kwargs):
    url = reverse_lazy(url_name, kwargs=kwargs)
    absolute_uri = settings.DOMAIN_URI + url
    return absolute_uri


