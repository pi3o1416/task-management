import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *
from . import CONFIG

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

#CSRF trusted origin
CSRF_TRUSTED_ORIGINS = []

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG["EMAIL_HOST"]
EMAIL_HOST_USER = CONFIG['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = CONFIG['EMAIL_HOST_PASSWORD']
EMAIL_PORT = CONFIG['EMAIL_PORT']
EMAIL_USE_TLS = CONFIG['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = CONFIG['DEFAULT_FROM_EMAIL']


# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_URL = 'redis://localhost:6379/'


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'tms'
    }
}


