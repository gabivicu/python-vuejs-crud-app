"""
Advanced ViewSet implementation for Django REST Framework.
- Custom queryset methods
- Caching
- Advanced filtering
- API documentation
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.utils import timezone
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer

# Optional: drf-spectacular for API documentation
try:
    from drf_spectacular.utils import extend_schema, OpenApiParameter
    from drf_spectacular.types import OpenApiTypes
    SPECTACULAR_AVAILABLE = True
except ImportError:
    # Fallback decorator if drf-spectacular is not installed
    def extend_schema(*args, **kwargs):
        def decorator(func):
            return func
        return decorator
    
    class OpenApiTypes:
        BOOL = 'boolean'
        STR = 'string'
    
    class OpenApiParameter:
        QUERY = 'query'
        
        def __init__(self, *args, **kwargs):
            # Accept any arguments but do nothing
            pass
    
    SPECTACULAR_AVAILABLE = False


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Item instances.
    
    Demonstrates:
    - Custom queryset methods
    - Advanced filtering and pagination
    - Caching for performance
    - API documentation with OpenAPI/Swagger
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='completed',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter by completion status',
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by category',
            ),
            OpenApiParameter(
                name='priority',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by priority',
            ),
            OpenApiParameter(
                name='search',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search in title, description, and tags',
            ),
            OpenApiParameter(
                name='due_filter',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by due date: overdue, today, upcoming',
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Order by field (prefix with - for descending)',
            ),
        ]
    )
    def get_queryset(self):
        """
        Optimized queryset using custom manager methods.
        Demonstrates query optimization and reusability.
        """
        queryset = Item.objects.all()
        
        # Use custom manager methods for better code organization
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            if completed.lower() == 'true':
                queryset = queryset.completed()
            else:
                queryset = queryset.pending()
        
        # Filter by category using manager method
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.by_category(category)
        
        # Filter by priority using manager method
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.by_priority(priority)
        
        # Search using custom manager method
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.search(search)
        
        # Filter by due date using manager methods
        due_filter = self.request.query_params.get('due_filter', None)
        if due_filter:
            if due_filter == 'overdue':
                queryset = queryset.overdue()
            elif due_filter == 'today':
                queryset = queryset.due_today()
            elif due_filter == 'upcoming':
                days = int(self.request.query_params.get('upcoming_days', 7))
                queryset = queryset.due_upcoming(days=days)
        
        # Ordering with validation
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            allowed_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'title']
            field = ordering.lstrip('-')
            if field in allowed_fields:
                queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    @extend_schema(
        summary="Get item statistics",
        description="Returns comprehensive statistics about items including counts by priority, category, and completion status.",
        responses={200: ItemSerializer}
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get statistics about items with caching.
        Demonstrates caching strategy for expensive queries.
        """
        cache_key = 'item_stats'
        cached_stats = cache.get(cache_key)
        
        if cached_stats is None:
            # Use custom manager methods for better performance
            total = Item.objects.count()
            completed = Item.objects.completed().count()
            pending = Item.objects.pending().count()
            overdue = Item.objects.overdue().count()
            
            # Count by priority using aggregation
            priority_stats = {}
            for priority_code, priority_name in Item.PRIORITY_CHOICES:
                priority_stats[priority_code] = Item.objects.by_priority(priority_code).count()
            
            # Count by category using aggregation
            category_stats = {}
            for category_code, category_name in Item.CATEGORY_CHOICES:
                category_stats[category_code] = Item.objects.by_category(category_code).count()
            
            completion_rate = (completed / total * 100) if total > 0 else 0
            
            cached_stats = {
                'total': total,
                'completed': completed,
                'pending': pending,
                'overdue': overdue,
                'completion_rate': round(completion_rate, 2),
                'priority_stats': priority_stats,
                'category_stats': category_stats,
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, cached_stats, 300)
        
        return Response(cached_stats)
    
    @extend_schema(
        summary="Get high priority pending items",
        description="Returns items with high or urgent priority that are not completed.",
    )
    @action(detail=False, methods=['get'])
    def high_priority_pending(self, request):
        """Get high priority pending items using custom manager method."""
        items = Item.objects.high_priority_pending()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Override create to add custom logic."""
        serializer.save()
        # Invalidate stats cache
        cache.delete('item_stats')
    
    def perform_update(self, serializer):
        """Override update to add custom logic."""
        serializer.save()
        # Invalidate stats cache
        cache.delete('item_stats')
    
    def perform_destroy(self, instance):
        """Override destroy to add custom logic."""
        instance.delete()
        # Invalidate stats cache
        cache.delete('item_stats')
