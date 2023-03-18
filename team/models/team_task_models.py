
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from services.mixins import ModelDeleteMixin, ModelUpdateMixin
from task.models import Task
from department.models import DepartmentMember
from .team_models import Team
from ..querysets import TeamTasksQuerySet
from ..exceptions import TeamTaskCreateFailed, TeamTaskDeleteFailed


class TeamTasks(ModelDeleteMixin, ModelUpdateMixin, models.Model):
    team = models.ForeignKey(
        to=Team,
        on_delete=models.CASCADE,
        related_name='team_tasks',
        verbose_name=_("Team"),
    )
    task = models.OneToOneField(
        primary_key=True,
        to=Task,
        on_delete=models.CASCADE,
        related_name='task_team',
        verbose_name=_("Task")
    )
    #Internal task are team taskes that is created by team leader and assign to a team member
    internal_task = models.BooleanField(
        verbose_name=_("Internal Task"),
        default=True,
    )
    objects = TeamTasksQuerySet.as_manager()
    class Meta:
        permissions = (('can_manage_team_tasks', _("Can Manage Team tasks"))),

    def clean(self, *args, **kwargs):
        #Validate if task is not internal task team member can not assign task to his own team
        if self.internal_task == False and self.team.members.filter(pk=self.task.created_by_id).exists():
            raise ValidationError("Team member can not assign task to his own team")
        #Validate task assignor has permission to create team task
        task_assignor = self.task.created_by
        if task_assignor.has_perm("team.add_teamtasks") != True:
            raise ValidationError("Task assignor does not have permission to create team task")
        #Validate task assignor department and team department should be equal
        task_assignor_department = DepartmentMember.objects.member_department(member_pk=self.task.created_by_id)
        team_department = self.team.department_id
        if task_assignor_department != team_department:
            raise ValidationError("Task assignor department and team department should be equal")

    def delete(self, *args, **kwargs):
        if self.task.status != Task.StatusChoices.PENDING:
            raise TeamTaskDeleteFailed("Task is already started by team members")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.clean(*args, **kwargs)
        super().save(*args, **kwargs)

    @classmethod
    def create_factory(cls, commit=False, **kwargs):
        try:
            assert kwargs.get('task') != None, "Task should not be empty"
            assert kwargs.get("team") != None, "Team should not be empty"
            team_task = cls(**kwargs)
            if commit == True:
                team_task.save()
            return team_task
        except AssertionError as exception:
            raise TeamTaskCreateFailed(detail=_(exception.__str__()))

    def create_subtask(self, commit=False, **kwargs):
        try:
            task = Task(**kwargs)
            if commit==True:
                task.save()
            return task
        except:
            pass





