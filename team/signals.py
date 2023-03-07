
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Team


@receiver(signal=pre_save, sender=Team)
def fill_team_lead_info(sender, instance, update_fields, **kwargs):
    if not update_fields:
        team_lead = instance.team_lead
        instance.team_lead_full_name = team_lead.full_name
        instance.team_lead_username = team_lead.username
    return  instance


@receiver(signal=pre_save, sender=Team)
def update_team_lead_info(sender, instance, update_fields, **kwargs):
    if update_fields and 'team_lead' in update_fields:
        team_lead = instance.team_lead
        instance.team_lead_full_name = team_lead.member_full_name
    return instance

