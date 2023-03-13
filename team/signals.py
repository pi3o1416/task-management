
from django.forms import model_to_dict
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from .exceptions import TeamLeadDeleteProhabited
from .models import Team
from . import tasks


@receiver(signal=post_save, sender=Team)
def add_team_lead_as_team_member(sender, instance:Team, update_fields, **kwargs):
    if not update_fields or 'team_lead' in update_fields:
        breakpoint()
        team_lead = instance.team_lead
        instance.members.add(team_lead)


@receiver(signal=m2m_changed, sender=Team.members.through)
def protect_team_lead_delete(sender, instance, action, pk_set, **kwargs):
    if action == 'pre_remove':
        team_lead = model_to_dict(instance).get('team_lead')
        if team_lead in pk_set:
            raise TeamLeadDeleteProhabited()


@receiver(signal=post_save, sender=Team)
def cache_team_data(sender, instance, **kwargs):
    tasks.cache_teams.delay()
