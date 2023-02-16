
from django.utils.translation import gettext_lazy as _
from django.db import models

from .exceptions import InvalidRequest

class ModelUpdateMixins(models.Model):
    class Meta:
        abstract=True

    def update(self, commit=True, **kwargs):
        assert self.error_messages, "Create error_messages field on your model"
        assert self.restricted_fields, "Add restricted_fields field on your model"
        previous_state = self
        fields = [field.name for field in self._meta.fields]
        for key, value in kwargs.items():
            if key in fields:
                setattr(self, key, value)
            else:
                self = previous_state
                raise InvalidRequest(detail={
                    "detail": _("{} {}".format(self.error_messages["UPDATE"]))
                })
        if commit == True:
            if self.pk != None:
                self.save(update_fields=kwargs.keys())
            else:
                self.save()
        return True


