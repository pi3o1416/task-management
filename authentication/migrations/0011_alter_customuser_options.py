# Generated by Django 4.1.3 on 2023-02-19 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['username'], 'permissions': (('can_view_all_users', 'Can View All User'), ('can_active_accont', 'Can Give Staff Permission To User'))},
        ),
    ]