
from django.contrib import admin

from .models import TaskAttachments, Task, UsersTasks, TaskTree


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]


@admin.register(TaskAttachments)
class TaskAttachmentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TaskAttachments._meta.fields]


@admin.register(UsersTasks)
class UsersTasksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UsersTasks._meta.fields]


@admin.register(TaskTree)
class TaskTreeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TaskTree._meta.fields]






