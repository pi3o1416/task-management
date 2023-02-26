
from django.db.models.deletion import RestrictedError
from django.utils.translation import gettext_lazy as _
from django.db import models

from .exceptions import TableEntityDeleteRestricted, InvalidFieldName, UpdateProhabitedField


class ModelUpdateMixin(models.Model):
    """
    Model mixin to Update a model instance
    declare error_messages with UPDATE key and restricted_fields on your model.
    """
    _error_messages = {
        "INVALID_KEY": "{} update faield. {} is an invalid field.",
        "RESTRICTED_FIELD": "{} update failed. {} is restricted field."
    }
    restricted_fields = ['pk']

    class Meta:
        abstract=True

    def update(self, commit=True, **kwargs):
        model_name = self.__class__.__name__
        fields = [field.name for field in self._meta.fields]
        for key, value in kwargs.items():
            if key not in fields:
                raise InvalidFieldName(
                    detail=_(self._error_messages["INVALID_KEY"].format(model_name, key))
                )
            if key in self.restricted_fields:
                raise UpdateProhabitedField(
                    detail=_(self._error_messages["RESTRICTED_FIELD"].format(model_name, key))
                )
            setattr(self, key, value)
        if commit == True:
            if self.pk == None:
                self.save()
            else:
                self.save(update_fields=kwargs.keys())
        return True


class ModelDeleteMixin(models.Model):
    """
    Model mixin to delete a model object
    declare error_messages field with DELETE field on your model
    """
    class Meta:
        abstract=True

    def delete(self):
        try:
            super().delete()
            return True
        except RestrictedError:
            raise TableEntityDeleteRestricted(
                detail=_("{} table entity delete restricted".format(self.__class__.__name__))
            )



