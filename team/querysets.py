
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _

from services.query_services import TemplateQuerySet


class TeamQuerySet(TemplateQuerySet):
    pass


class TeamMemberQuerySet(TemplateQuerySet):
    def bulk_create_team_member(self, team_members):
        Model = self.model
        team_members = [pre_save.send(Model, instance=team_member, update_fields=None)[0][1] for team_member in team_members]
        breakpoint()
        team_members = Model.objects.bulk_create(team_members)
        return team_members


class TeamTasksQuerySet(TemplateQuerySet):
    pass


