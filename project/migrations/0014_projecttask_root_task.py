# Generated by Django 4.1.3 on 2023-03-16 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_delete_projectschemalessdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttask',
            name='root_task',
            field=models.BooleanField(default=False, verbose_name='Created by Project maintainer'),
        ),
    ]
