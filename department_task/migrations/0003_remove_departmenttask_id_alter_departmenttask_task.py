# Generated by Django 4.1.3 on 2023-03-19 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0023_remove_userstasks_id_alter_userstasks_task'),
        ('department_task', '0002_alter_departmenttask_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departmenttask',
            name='id',
        ),
        migrations.AlterField(
            model_name='departmenttask',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='assigned_to_dept', serialize=False, to='task.task', verbose_name='Task'),
        ),
    ]
