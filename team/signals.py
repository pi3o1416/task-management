
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import Team


@receiver(signal=post_save, sender=Team)
def fill_team_lead_info(sender, instance, created, **kwargs):
    if created:
        team_lead = instance.team_lead
        instance.team_lead_full_name = team_lead.member_full_name
        instance.save()




