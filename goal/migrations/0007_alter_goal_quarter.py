# Generated by Django 4.1.3 on 2023-01-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0006_alter_goal_completion_alter_goal_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='quarter',
            field=models.IntegerField(choices=[(1, 'Quarter 1'), (2, 'Quarter 2'), (3, 'Quarter 3'), (4, 'Quarter 4')], verbose_name='Year Quarter'),
        ),
    ]
