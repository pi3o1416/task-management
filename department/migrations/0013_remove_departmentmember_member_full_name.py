# Generated by Django 4.1.3 on 2023-02-22 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0012_alter_departmentmember_designation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departmentmember',
            name='member_full_name',
        ),
    ]