
from functools import reduce
from operator import __and__
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, APIException
from rest_framework.request import Request

from services.query_services import generate_q_objects_from_query_params



class TeamQuerySet(QuerySet):
    def get_team_by_pk(self, pk):
        try:
            team = self.get(pk=pk)
            return team
        except self.model.DoesNotExist:
            raise NotFound(detail=_("Team with pk={} does not exist".format(pk)))
        except ValueError:
            raise NotFound(detail=_("Team pk should be integer"))
        except Exception as exception:
            raise NotFound(detail=_(exception.__str__()))

    def filter_from_query_params(self, request: Request):
       try:
           q_objects = generate_q_objects_from_query_params(self.model, request)
           if q_objects:
               return self.filter(reduce(__and__, q_objects))
           return self.all()
       except Exception as exception:
           raise APIException(detail={"detail": exception.args})



