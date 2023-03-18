
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from .models import TaskTree, UsersTasks, Task


@receiver(signal=post_save, sender=TaskTree)
def change_has_subtask_true(sender, instance:TaskTree, created, **kwargs):
    if created:
        parent = instance.parent
        if parent.has_subtask != True:
            parent.update(has_subtask=True, commit=True)

@receiver(signal=post_delete, sender=TaskTree)
def change_has_subtask_false(sender, instance:TaskTree, **kwargs):
    parent = instance.parent
    parent_has_subtask = TaskTree.objects.filter(parent=parent).exists()
    if parent_has_subtask == False:
        parent.update(has_subtask=False, commit=True)
    else:
        if parent.has_subtask == False:
            parent.update(has_subtask=True, commit=True)


@receiver(signal=pre_save, sender=Task)
def make_task_approved_by_default(sender, instance:Task, **kwargs):
    if instance.pk == None:
        created_by = instance.created_by
        if created_by.has_perm("task.can_approve_disapprove_task"):
            instance.approval_status = Task.ApprovalChoices.APPROVED
    return instance

