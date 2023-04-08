
<<<<<<< HEAD
=======
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
>>>>>>> 067b979 (Configure sentry support.)
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tmsv2.aamarpay.com', '127.0.0.1']

#Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = CONFIG['EMAIL_HOST_USER']

#Domain
DOMAIN_URI = "http://127.0.0.1:8000"


# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_EXTENDED = True

<<<<<<< HEAD





=======
#Configuration for sentry
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
    send_default_pii=True
)
>>>>>>> 067b979 (Configure sentry support.)
