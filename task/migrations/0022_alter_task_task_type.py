# Generated by Django 4.1.3 on 2023-03-15 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0021_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('RGT', 'Regular task'), ('DPT', 'Department task'), ('PRT', 'Project task'), ('TMT', 'Team task')], default='RGT', max_length=3, verbose_name='Task type'),
        ),
    ]
