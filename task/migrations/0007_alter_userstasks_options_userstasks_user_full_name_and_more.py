# Generated by Django 4.1.3 on 2023-01-18 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_alter_task_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userstasks',
            options={'permissions': (('can_view_inter_department_task', 'Can View Inter Department Tasks'), ('can_view_all_tasks', 'Can View All Tasks'))},
        ),
        migrations.AddField(
            model_name='userstasks',
            name='user_full_name',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='User fullname'),
        ),
        migrations.AddField(
            model_name='userstasks',
            name='user_username',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='User username'),
        ),
    ]
