"""
Service layer for business logic.
Demonstrates separation of concerns and service-oriented architecture.
"""
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone
from .models import Item


class ItemService:
    """Service class for Item business logic."""
    
    @staticmethod
    def get_statistics():
        """
        Get comprehensive statistics about items.
        Uses caching for performance optimization.
        """
        cache_key = 'item_statistics'
        cached_stats = cache.get(cache_key)
        
        if cached_stats is None:
            stats = {
                'total': Item.objects.count(),
                'completed': Item.objects.completed().count(),
                'pending': Item.objects.pending().count(),
                'overdue': Item.objects.overdue().count(),
                'due_today': Item.objects.due_today().count(),
                'high_priority_pending': Item.objects.high_priority_pending().count(),
            }
            
            # Priority distribution
            priority_stats = {}
            for priority_code, _ in Item.PRIORITY_CHOICES:
                priority_stats[priority_code] = Item.objects.by_priority(priority_code).count()
            stats['priority_stats'] = priority_stats
            
            # Category distribution
            category_stats = {}
            for category_code, _ in Item.CATEGORY_CHOICES:
                category_stats[category_code] = Item.objects.by_category(category_code).count()
            stats['category_stats'] = category_stats
            
            # Completion rate
            if stats['total'] > 0:
                stats['completion_rate'] = round(
                    (stats['completed'] / stats['total']) * 100, 2
                )
            else:
                stats['completion_rate'] = 0
            
            # Cache for 5 minutes
            cache.set(cache_key, stats, 300)
            cached_stats = stats
        
        return cached_stats
    
    @staticmethod
    def invalidate_statistics_cache():
        """Invalidate statistics cache."""
        cache.delete('item_statistics')
    
    @staticmethod
    def search_items(query, filters=None):
        """
        Advanced search with multiple filters.
        
        Args:
            query: Search query string
            filters: Dictionary of filters (category, priority, completed, etc.)
        
        Returns:
            QuerySet of matching items
        """
        queryset = Item.objects.search(query) if query else Item.objects.all()
        
        if filters:
            if filters.get('category'):
                queryset = queryset.by_category(filters['category'])
            if filters.get('priority'):
                queryset = queryset.by_priority(filters['priority'])
            if filters.get('completed') is not None:
                if filters['completed']:
                    queryset = queryset.completed()
                else:
                    queryset = queryset.pending()
            if filters.get('due_filter') == 'overdue':
                queryset = queryset.overdue()
            elif filters.get('due_filter') == 'today':
                queryset = queryset.due_today()
        
        return queryset
    
    @staticmethod
    def bulk_update_status(item_ids, completed):
        """
        Bulk update item completion status.
        
        Args:
            item_ids: List of item IDs
            completed: Boolean completion status
        
        Returns:
            Number of updated items
        """
        updated = Item.objects.filter(id__in=item_ids).update(completed=completed)
        ItemService.invalidate_statistics_cache()
        return updated
    
    @staticmethod
    def bulk_delete(item_ids):
        """
        Bulk delete items.
        
        Args:
            item_ids: List of item IDs
        
        Returns:
            Number of deleted items
        """
        deleted_count, _ = Item.objects.filter(id__in=item_ids).delete()
        ItemService.invalidate_statistics_cache()
        return deleted_count
