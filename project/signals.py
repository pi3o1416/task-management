
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

from services.exceptions import DBOperationFailed, InvalidRequest
from .models import Project, ProjectSchemaLessData


@receiver(signal=post_save, sender=Project)
def create_project_schemaless_data(sender, instance:Project, created=None, **kwargs):
    if created:
        try:
            ProjectSchemaLessData.create_factory(
                commit=True,
                project = instance,
                department_title = instance.department.name,
                project_owner_fullname = instance.project_owner.full_name,
                project_owner_username = instance.project_owner.username,
                project_manager_fullname = instance.project_manager.full_name,
                project_manager_username = instance.project_manager.username,
            )
        except InvalidRequest:
            instance.delete()
            raise DBOperationFailed(detail={"detail":_("Project create cancled due to Project optional data update filed")})


@receiver(signal=post_save, sender=Project)
def update_project_schemaless_data(sender, instance:Project, created=None, update_fields=None, **kwargs):
    if update_fields:
        schemaless_data = ProjectSchemaLessData.objects.get(project=instance)
        if 'department' in update_fields:
            schemaless_data.department_title = instance.department.name
        if 'project_manager' in update_fields:
            schemaless_data.project_manager_username = instance.project_manager.username
            schemaless_data.project_manager_fullname = instance.project_manager.full_name
        if 'project_owner' in update_fields:
            schemaless_data.project_owner_username = instance.project_owner.username
            schemaless_data.project_onwer_fullname = instance.project_owner.full_name
        schemaless_data.save()


@receiver(signal=post_save, sender=Project)
def add_project_manager_as_project_member(sender, instance:Project, created=None, update_fields=None, **kwargs):
    if created:
        project_manager = instance.project_manager
        instance.members.add(project_manager)










