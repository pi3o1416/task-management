# Generated by Django 4.1.3 on 2023-03-09 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0011_remove_team_team_lead_full_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'permissions': (('can_view_all_teams', 'Can View All Teams'),)},
        ),
    ]