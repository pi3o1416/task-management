
from django.contrib import admin
from .models import Team, TeamMember, TeamTasks


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'team_lead', 'department']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['pk', 'team', 'member', 'member_full_name', 'member_username']


@admin.register(TeamTasks)
class TeamTasksAdmin(admin.ModelAdmin):
    list_display = ['pk', 'team', 'task']

