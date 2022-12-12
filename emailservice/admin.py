from django.contrib import admin
from .models import EmailHistory
from django_celery_results.models import TaskResult

# Register your models here.

@admin.register(EmailHistory)
class EmailHistoryAdmin(admin.ModelAdmin):
    list_display = ['email_subject', 'email_to', 'email_status', 'created_at',  'email_task']


