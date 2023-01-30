
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


class TeamQuerySet(QuerySet):
    def get_team_by_pk(self, pk):
        try:
            team = self.get(pk)
        except self.model.DoesNotExist:
            raise NotFound(detail=_("Team with pk={} does not exist".format(pk)))
        except ValueError:
            raise NotFound(detail=_("Team pk should be integer"))
        except Exception as exception:
            raise NotFound(detail=_(exception.__str__()))
