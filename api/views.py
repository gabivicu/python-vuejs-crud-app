from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from .models import Item
from .serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Item instances.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        
        # Filter by completion status
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Search by title or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search) | Q(tags__icontains=search)
            )
        
        # Filter by due date (overdue, today, upcoming)
        due_filter = self.request.query_params.get('due_filter', None)
        if due_filter:
            now = timezone.now()
            if due_filter == 'overdue':
                queryset = queryset.filter(due_date__lt=now, completed=False)
            elif due_filter == 'today':
                queryset = queryset.filter(due_date__date=now.date(), completed=False)
            elif due_filter == 'upcoming':
                queryset = queryset.filter(due_date__gt=now, completed=False)
        
        # Ordering
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            allowed_fields = ['created_at', 'updated_at', 'due_date', 'priority', 'title']
            if ordering.lstrip('-') in allowed_fields:
                queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get statistics about items."""
        total = Item.objects.count()
        completed = Item.objects.filter(completed=True).count()
        pending = Item.objects.filter(completed=False).count()
        
        # Count by priority
        priority_stats = {}
        for priority_code, priority_name in Item.PRIORITY_CHOICES:
            priority_stats[priority_code] = Item.objects.filter(priority=priority_code).count()
        
        # Count by category
        category_stats = {}
        for category_code, category_name in Item.CATEGORY_CHOICES:
            category_stats[category_code] = Item.objects.filter(category=category_code).count()
        
        # Overdue items
        overdue = Item.objects.filter(due_date__lt=timezone.now(), completed=False).count()
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return Response({
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completion_rate': round(completion_rate, 2),
            'priority_stats': priority_stats,
            'category_stats': category_stats,
        })

