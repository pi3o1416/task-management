# Generated by Django 4.1.3 on 2023-03-09 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0012_alter_team_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamtasks',
            name='internal_task',
            field=models.BooleanField(default=True, verbose_name='Internal Task'),
        ),
    ]
