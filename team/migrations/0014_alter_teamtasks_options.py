# Generated by Django 4.1.3 on 2023-03-16 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0013_teamtasks_internal_task'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='teamtasks',
            options={'permissions': (('can_manage_team_tasks', 'Can Manage Team tasks'),)},
        ),
    ]
