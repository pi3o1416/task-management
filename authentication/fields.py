
from urllib.parse import urljoin
from django.conf import settings
from django.db.models.fields.files import ImageField, ImageFieldFile


class CustomImageFieldFile(ImageFieldFile):
    def __str__(self):
        if self.url:
            return urljoin(settings.DOMAIN_URI, self.url)
        return ''


class CustomImageField(ImageField):
    attr_class = CustomImageFieldFile
