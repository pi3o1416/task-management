# Generated by Django 4.1.3 on 2023-02-01 06:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0004_team_team_lead_username_alter_team_team_lead'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Member full name')),
                ('member_username', models.CharField(blank=True, max_length=200, null=True, verbose_name='Member username')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_teams', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_members', to='team.team')),
            ],
        ),
    ]
