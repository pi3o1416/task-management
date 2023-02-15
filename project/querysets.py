
from services.querysets import TemplateQuerySet, get_model_foreignkey_fields


class ProjectQuerySet(TemplateQuerySet):
    def filter_with_reverse_related_fields(self, request):
        filtered_projects = self.select_related('schemaless_data').filter_from_query_params(request=request)
        for related_object in self.model._meta.related_objects:
            FieldModel = related_object.field.model
            field_name = related_object.name
            filtered_projects = filtered_projects.filter_from_query_params(request=request, FieldModel=FieldModel, related_field=field_name)
        return filtered_projects


class ProjectAttachmentQuerySet(TemplateQuerySet):
    pass





