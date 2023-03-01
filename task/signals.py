
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import TaskTree, UsersTasks, Task

@receiver(signal=post_save, sender=UsersTasks)
def update_task_type_to_user_task(sender, instance:UsersTasks, created, **kwargs):
    if created:
        task = instance.task
        if task.task_type != Task.TaskType.USER_TASK:
            task.update(
                task_type = Task.TaskType.USER_TASK,
                is_assigned = True,
                commit=True
            )

@receiver(signal=post_delete, sender=UsersTasks)
def update_task_type_to_undetermine(sender, instance:UsersTasks, **kwargs):
    task = instance.task
    task.update(
        task_type = Task.TaskType.NONE,
        is_assigned = False,
        commit=True
    )

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












