# Generated by Django 4.1.3 on 2022-12-08 10:49

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('emailservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='emailhistory',
            managers=[
                ('email_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
