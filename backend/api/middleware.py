from django.conf import settings
from django.http import HttpResponse


class ApiCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "OPTIONS" and request.path.startswith("/api/"):
            response = HttpResponse()
        else:
            response = self.get_response(request)

        if request.path.startswith("/api/"):
            origin = request.headers.get("Origin")
            allowed_origins = set(getattr(settings, "CORS_ALLOWED_ORIGINS", []))

            if getattr(settings, "CORS_ALLOW_ALL_ORIGINS", False):
                response["Access-Control-Allow-Origin"] = origin or "*"
            elif origin in allowed_origins:
                response["Access-Control-Allow-Origin"] = origin

            if "Access-Control-Allow-Origin" in response:
                response["Vary"] = "Origin"
                response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
                response["Access-Control-Allow-Headers"] = "Content-Type"

        return response
