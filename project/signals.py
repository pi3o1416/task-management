
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save

from services.exceptions import DBOperationFailed, InvalidRequest
from .models import Project, ProjectSchemaLessData


@receiver(signal=post_save, sender=Project)
def update_project_schemaless_data(sender, instance:Project, created=None, **kwargs):
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
            raise DBOperationFailed(detail={"detail":_("Project optional data update filed")})



