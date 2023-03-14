from django.contrib import admin
from django.contrib.auth.models import Permission

# Register your models here.


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'content_type', 'codename']
    list_filter = ['content_type__model']




