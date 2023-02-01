
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models import Team, TeamMember


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


@receiver(signal=pre_save, sender=TeamMember)
def fill_team_member_info(sender, instance, update_fields, **kwargs):
    if not update_fields:
        member = instance.member
        instance.member_full_name = member.full_name
        instance.member_username = member.username
    return instance



@receiver(signal=post_save, sender=Team)
def add_team_lead_as_team_member(sender, instance, update_fields, **kwargs):
    if not update_fields or 'team_lead' in update_fields:
        team_member = TeamMember.create_factory(commit=False, team=instance, member=instance.team_lead)
        team_member.save()
        return team_member



