
from django.contrib import admin
from .models import Team, TeamTasks


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'team_lead', 'department', 'get_members']

    def get_members(self, team:Team):
        team_members = team.members.all()
        if team_members:
            return [member.username for member in team_members]
        return None


@admin.register(TeamTasks)
class TeamTasksAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TeamTasks._meta.fields]


