
from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        custom_data = {
            "data": None,
            "error": None,
            "status": None,
        }
        response = renderer_context.get("response")
        custom_data["status"] = response.status_code
        if response.status_code >= 400:
            custom_data["error"] = data
        else:
            custom_data["data"] = data
        return super().render(custom_data, accepted_media_type, renderer_context)





