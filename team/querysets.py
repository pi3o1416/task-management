
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _

from services.querysets import TemplateQuerySet, get_model_foreignkey_fields


class TeamQuerySet(TemplateQuerySet):
    pass


class TeamMemberQuerySet(TemplateQuerySet):
    def bulk_create_team_member(self, team_members):
        Model = self.model
        team_members = [pre_save.send(Model, instance=team_member, update_fields=None)[0][1] for team_member in team_members]
        team_members = Model.objects.bulk_create(team_members)
        return team_members


class TeamTasksQuerySet(TemplateQuerySet):
    def filter_with_related_fields(self, request):
        #TODO: Update name to filter with foreignkey field
        #Default filter
        filtered_tasks = self.filter_from_query_params(request=request)
        #Filter for foreignkey relation
        for field in get_model_foreignkey_fields(self.model):
            FieldModel = field.remote_field.model
            field_name = field.name
            filtered_tasks = self.filter_from_query_params(request=request, FieldModel=FieldModel, related_field=field_name)
        return filtered_tasks




