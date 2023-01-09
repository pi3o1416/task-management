
from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        custom_data = {
            "response_data": None,
            "error": None,
            "status": None,
        }
        response = renderer_context.get("response")
        custom_data["status"] = response.status_code
        if response.status_code >= 400:
            custom_data["error"] = {
                "detail": None,
                "field_errors": None
            }
            detail = data.get("detail")
            field_errors = data.get("field_errors")
            if detail:
                custom_data["error"]["detail"] = detail
            if field_errors:
                custom_data["error"]["field_errors"] = field_errors
            if not detail and not field_errors:
                custom_data["error"]["detail"] = data
        else:
            custom_data["response_data"] = data
        return super().render(custom_data, accepted_media_type, renderer_context)





