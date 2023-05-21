# Generated by Django 4.1.3 on 2023-03-27 06:06

import authentication.fields
import authentication.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=authentication.fields.CustomImageField(blank=True, null=True, upload_to=authentication.models.user_photo_upload_path, verbose_name='User photo'),
        ),
    ]