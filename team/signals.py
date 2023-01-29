
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Team


@receiver(signal=pre_save, sender=Team)
def fill_team_lead_info(sender, instance, created, **kwarge):
    if created:
        team_lead = instance.team_lead
        instance.team_lead_username = team_lead.username
        instance.team_lead_first_name = team_lead.first_name
        instance.team_lead_last_name = team_lead.last_name
        return instance


