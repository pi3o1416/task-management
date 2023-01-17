
from operator import __and__
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound

def get_group_by_pk(pk):
    try:
        group = Group.objects.get(pk=pk)
        return group
    except Group.DoesNotExist:
        raise NotFound({"detail": [_("Group with pk={} does not exist".format(pk))]})
    except ValueError:
        raise NotFound({"detail": [_("Group pk should be an integer")]})
    except Exception as exception:
        raise NotFound({"detail": exception.args})

























