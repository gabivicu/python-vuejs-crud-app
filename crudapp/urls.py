"""
URL configuration for crudapp project.
"""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def api_root(request):
    """Root endpoint providing API information."""
    endpoints = {
        "items": "/api/items/",
        "admin": "/admin/",
    }

    # Add API docs endpoints if available
    try:
        from drf_spectacular.views import (  # noqa: F401
            SpectacularAPIView,
            SpectacularRedocView,
            SpectacularSwaggerView,
        )

        endpoints.update(
            {
                "api_docs": "/api/schema/",
                "swagger": "/api/schema/swagger-ui/",
                "redoc": "/api/schema/redoc/",
            }
        )
    except ImportError:
        pass

    return JsonResponse(
        {
            "message": "Welcome to Django CRUD API",
            "endpoints": endpoints,
            "documentation": {
                "GET /api/items/": "List all items",
                "POST /api/items/": "Create a new item",
                "GET /api/items/{id}/": "Get a specific item",
                "PUT /api/items/{id}/": "Update an item",
                "DELETE /api/items/{id}/": "Delete an item",
            },
        }
    )


urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]

# Add API documentation URLs if drf-spectacular is available
try:
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
except ImportError:
    pass
