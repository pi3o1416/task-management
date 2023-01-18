
from django.contrib import admin

from .models import TaskAttachments, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]


@admin.register(TaskAttachments)
class TaskAttachmentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TaskAttachments._meta.fields]






