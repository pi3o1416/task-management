
from django.utils.translation import gettext_lazy as _
from django.db import models

from .exceptions import InvalidRequest

class ModelUpdateMixins(models.Model):
    class Meta:
        abstract=True

    def update(self, commit=True, **kwargs):
        assert hasattr(self, 'error_messages'), "Create error_messages field on your model"
        assert hasattr(self, 'restricted_fields'), "Add restricted_fields field on your model"
        assert type(self.error_messages) is type(dict()), "error_messages field should be an dict"
        assert "UPDATE" in self.error_messages, "UPDATE key is absent from error_messages dictionary"
        fields = [field.name for field in self._meta.fields]
        for key, value in kwargs.items():
            if key not in fields:
                raise InvalidRequest(detail={
                    "detail": _("{} {} is an invalid field".format(self.error_messages["UPDATE"], key))
                })
            if key in self.restricted_fields:
                raise InvalidRequest(detail={
                    "detail": _("{} {} is prohabited from any update".format(self.error_messages["UPDATE"], key))
                })
            setattr(self, key, value)
        if commit == True:
            if self.pk == None:
                self.save()
            else:
                self.save(update_fields=kwargs.keys())
        return True


