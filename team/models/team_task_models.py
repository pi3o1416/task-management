
from django.db import models
from django.utils.translation import gettext_lazy as _

from services.mixins import ModelDeleteMixin, ModelUpdateMixin
from task.models import Task
from .team_models import Team
from ..querysets import TeamTasksQuerySet
from ..exceptions import TeamTaskCreateFailed


class TeamTasks(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        related_name='team_tasks',
        verbose_name=_("Team"),
    )
    task = models.OneToOneField(
        to=Task,
        on_delete=models.CASCADE,
        related_name='task_team',
        verbose_name=_("Task")
    )
    objects = TeamTasksQuerySet.as_manager()
    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            assert kwargs.get('task') != None, "Task should not be empty"
            assert kwargs.get("team") != None, "Team should not be empty"
            team_task = cls(**kwargs)
            if commit == True:
                team_task.save()
            return team_task
        except Exception as exception:
            raise TeamTaskCreateFailed(detail=_(exception.__str__()))

    def create_subtask(self, commit=False, **kwargs):
        try:
            task = Task(**kwargs)
            if commit==True:
                task.save()
            return task
        except:
            pass





