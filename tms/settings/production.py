import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .base import *
from . import CONFIG

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tmsv2-backend.aamarpay.xyz']

#CSRF trusted origin
CSRF_TRUSTED_ORIGINS = ['tmsv2-backend.aamarpay.xyz']

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = CONFIG['EMAIL_HOST_USER']

# Domain
DOMAIN_URI = "https://tmsv2.aamarpay.com"

# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_URL = 'redis://system_redis:6379/'

# Configuration for sentry
sentry_sdk.init(
    dsn="https://a1ff75fa9a95483693c31dea9957c4f3@o1182560.ingest.sentry.io/4504327056850944",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    in_app_exclude=['flower']
)
