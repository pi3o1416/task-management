
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['testserver', '127.0.0.1']

# Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG["EMAIL_HOST"]
EMAIL_HOST_USER = CONFIG['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = CONFIG['EMAIL_HOST_PASSWORD']
EMAIL_PORT = CONFIG['EMAIL_PORT']
EMAIL_USE_TLS = CONFIG['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = CONFIG['DEFAULT_FROM_EMAIL']


#Domain
DOMAIN_URI = "http://127.0.0.1:8000"


# Celery Configuration Options
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_URL = 'redis://localhost:6379/'


INTERNAL_IPS = [
    "127.0.0.1",
]


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
















>>>>>>> 765005b (Remove sentry support for dev branch.)

