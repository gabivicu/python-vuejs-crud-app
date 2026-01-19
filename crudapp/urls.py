"""
URL configuration for crudapp project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root(request):
    """Root endpoint providing API information."""
    return JsonResponse({
        'message': 'Welcome to Django CRUD API',
        'endpoints': {
            'items': '/api/items/',
            'admin': '/admin/',
        },
        'documentation': {
            'GET /api/items/': 'List all items',
            'POST /api/items/': 'Create a new item',
            'GET /api/items/{id}/': 'Get a specific item',
            'PUT /api/items/{id}/': 'Update an item',
            'DELETE /api/items/{id}/': 'Delete an item',
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

