
from django.contrib import admin

from .models import Project, ProjectSchemaLessData, ProjectAttachment, ProjectTask


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'description', 'deadline', 'budget', 'project_manager',
                    'project_owner', 'department', 'status', 'get_members']

    def get_members(self, project:Project):
        project_members = project.members.all()
        if project_members:
            return [member.username for member in project_members]
        return project.title


@admin.register(ProjectSchemaLessData)
class ProjectSchemaLessDataAdmin(admin.ModelAdmin):
    list_display = ['pk', 'project', 'department_title', 'project_owner_fullname',
                    'project_owner_username', 'project_manager_fullname',
                    'project_manager_username']


@admin.register(ProjectAttachment)
class ProjectAttachmentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'project', 'attached_by', 'attachment', 'attached_by',
                    'attached_by_user_username', 'attached_by_user_fullname']


@admin.register(ProjectTask)
class ProjectTaskAdmin(admin.ModelAdmin):
    list_display = ['pk', 'project', 'task']













