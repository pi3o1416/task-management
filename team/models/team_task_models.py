
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from services.mixins import ModelDeleteMixin, ModelUpdateMixin
from task.models import Task, TaskTree, UsersTasks
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
    root_task = models.BooleanField(
        verbose_name=_("Team root task"),
        default=False
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
        #Validate if internal task == False root task == False
        if self.internal_task == False and self.root_task != False:
            raise ValidationError("Team If internal task == False root task needs to be False")
        #Validate if task is not internal task team member can not assign task to his own team
        if self.internal_task == False and self.team.members.filter(pk=self.task.created_by_id).exists():
            raise ValidationError("Team member can not assign task to his own team")
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
    def create_factory(cls, commit=True, **kwargs):
        try:
            assert kwargs.get('task') != None, "Task should not be empty"
            assert kwargs.get("team") != None, "Team should not be empty"
            team_task = cls(**kwargs)
            if commit == True:
                team_task.save()
            return team_task
        except AssertionError as exception:
            raise TeamTaskCreateFailed(detail=_(exception.__str__()))

    @classmethod
    def assign_task_on_team(cls, team:Team, task:Task, commit=True):
        if task.TaskType == Task.TaskType.TEAM_TASK:
            task_team = task.task_team
            task_team.update(team=team, commit=True)
        team_task = cls.create_factory(
            commit=True,
            team=team,
            task=task,
            root_task=False,
            internal_task=False
        )
        return team_task


    @classmethod
    def create_root_task(cls, commit=True, **kwargs):
        assert kwargs.get('root_task') == None, "Root task should not given as method parameter"
        assert kwargs.get('internal_task') == None, "Internal task should not be given as method perameter"
        return cls.create_factory(
            commit=commit,
            root_task=True,
            internal_task=True,
            **kwargs
        )

    @transaction.atomic
    @classmethod
    def create_and_assign_root_task(cls, assigned_to, commit=True, **kwargs):
        team_task = cls.create_root_task(commit=commit, **kwargs)
        user_task = UsersTasks.create_factory(commit=True, assigned_to=assigned_to, task=team_task.task)
        return user_task


    @transaction.atomic
    def create_subtask(self, child_task:Task, commit=True):
        team = self.team
        TaskTree.create_factory(
            commit=commit,
            parent=self.task,
            child=child_task
        )
        child_team_task = TeamTasks.create_factory(
            commit=True,
            team=team,
            task=child_task,
            root_task= True if self.internal_task == False else False,
            internal_task=True,
        )
        return child_team_task

    @transaction.atomic
    def create_and_assign_subtask(self, child_task, assigned_to, commit=True):
        self.create_subtask(child_task=child_task)
        user_task = UsersTasks.create_factory(
            commit=commit,
            assigned_to=assigned_to,
            task=child_task
        )
        return user_task



