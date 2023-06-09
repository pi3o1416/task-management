# Generated by Django 4.1.3 on 2023-01-22 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0011_remove_task_approved_by_dept_head_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'permissions': (('can_approve_disapprove_task', 'Can Approve Or Disapprove Tasks'), ('can_view_all_tasks', 'Can View All Tasks'))},
        ),
        migrations.AlterModelOptions(
            name='userstasks',
            options={'permissions': (('can_view_inter_department_task', 'Can View Inter Department Tasks'), ('can_view_all_users_tasks', 'Can View All Users Tasks'))},
        ),
    ]
