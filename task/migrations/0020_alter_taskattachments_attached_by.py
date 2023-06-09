# Generated by Django 4.1.3 on 2023-03-02 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0019_remove_userstasks_user_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskattachments',
            name='attached_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_files', to=settings.AUTH_USER_MODEL, verbose_name='Attached by'),
        ),
    ]
