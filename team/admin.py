
from django.contrib import admin
from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'team_lead', 'department']
