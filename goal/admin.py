
from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GloadAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'year', 'quarter', 'review_status', 'review', 'completion']









