
from django.contrib import admin
from .models import Team, TeamTasks


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'team_lead', 'department']


@admin.register(TeamTasks)
class TeamTasksAdmin(admin.ModelAdmin):
    list_display = ['pk', 'team', 'task']

