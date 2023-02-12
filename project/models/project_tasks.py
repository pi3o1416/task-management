
from django.db import models
from django.utils.translation import gettext_lazy as _

from services.exceptions import InvalidRequest, DBOperationFailed
from task.models import Task
from .project_models import Project
from ..validators import validate_project_task_type



class ProjectTask(models.Model):
    error_messages = {
        "CREATE": "Project task create failed.",
        "UPDATE": "Project task update failed.",
        "DELETE": "Project task delete failed.",
        "RETRIEVE": "Project task retrieve failed.",
        "PATCH": "Project task patch failed.",
    }

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='project_tasks',
        verbose_name=_("Project")
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        related_name='task_project',
        verbose_name=_("Task"),
        validators=[validate_project_task_type]
    )

    @classmethod
    def create_factory(cls, commit=True, **kwargs):
        try:
            project_task = cls(**kwargs)
            if commit:
                project_task.save()
            return project_task
        except Exception as exception:
            raise InvalidRequest(detail={
                "detail": _(cls.error_messages["CREATE"] + exception.__str__())
            })

    def delete(self):
        try:
            super().delete()
            return True
        except Exception as exception:
            raise DBOperationFailed(detail={
                "detail": _(self.error_messages["DELETE"] + exception.__str__())
            })


