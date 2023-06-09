# Generated by Django 4.1.3 on 2023-02-05 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0016_task_has_subtask'),
        ('team', '0007_teamtasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamtasks',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='task_team', to='task.task', verbose_name='Task'),
        ),
    ]
