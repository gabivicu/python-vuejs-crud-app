"""
Custom managers and querysets for advanced query operations.
"""
from django.db import models
from django.db.models import Q, Count, Avg, F
from django.utils import timezone
from datetime import timedelta


class ItemQuerySet(models.QuerySet):
    """Custom queryset with advanced filtering methods."""
    
    def completed(self):
        """Return only completed items."""
        return self.filter(completed=True)
    
    def pending(self):
        """Return only pending items."""
        return self.filter(completed=False)
    
    def overdue(self):
        """Return overdue items."""
        return self.filter(
            due_date__lt=timezone.now(),
            completed=False
        )
    
    def due_today(self):
        """Return items due today."""
        today = timezone.now().date()
        return self.filter(
            due_date__date=today,
            completed=False
        )
    
    def due_upcoming(self, days=7):
        """Return items due in the next N days."""
        now = timezone.now()
        future = now + timedelta(days=days)
        return self.filter(
            due_date__gte=now,
            due_date__lte=future,
            completed=False
        )
    
    def by_priority(self, priority):
        """Filter by priority level."""
        return self.filter(priority=priority)
    
    def by_category(self, category):
        """Filter by category."""
        return self.filter(category=category)
    
    def search(self, query):
        """Full-text search across title, description, and tags."""
        return self.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    
    def with_stats(self):
        """Annotate queryset with statistics."""
        return self.annotate(
            days_until_due=models.Case(
                models.When(
                    due_date__isnull=False,
                    then=F('due_date') - timezone.now()
                ),
                default=None,
                output_field=models.DurationField()
            )
        )
    
    def high_priority_pending(self):
        """Return high or urgent priority pending items."""
        return self.filter(
            priority__in=['high', 'urgent'],
            completed=False
        )


class ItemManager(models.Manager):
    """Custom manager for Item model."""
    
    def get_queryset(self):
        """Return custom queryset."""
        return ItemQuerySet(self.model, using=self._db)
    
    def completed(self):
        """Return completed items."""
        return self.get_queryset().completed()
    
    def pending(self):
        """Return pending items."""
        return self.get_queryset().pending()
    
    def overdue(self):
        """Return overdue items."""
        return self.get_queryset().overdue()
    
    def due_today(self):
        """Return items due today."""
        return self.get_queryset().due_today()
    
    def search(self, query):
        """Search items."""
        return self.get_queryset().search(query)
    
    def by_priority(self, priority):
        """Filter by priority level."""
        return self.get_queryset().by_priority(priority)
    
    def by_category(self, category):
        """Filter by category."""
        return self.get_queryset().by_category(category)
    
    def high_priority_pending(self):
        """Return high priority pending items."""
        return self.get_queryset().high_priority_pending()
