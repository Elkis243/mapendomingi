"""Middleware SEO / protection crawl."""


class AdminRobotsNoIndexMiddleware:
    """Empêche l'indexation de l'admin même si un bot ignore robots.txt."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if path.startswith("/admin/") or path == "/admin":
            response["X-Robots-Tag"] = "noindex, nofollow, noarchive"
        return response
