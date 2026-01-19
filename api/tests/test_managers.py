"""
Unit tests for custom managers and querysets.
Demonstrates testing of advanced Django patterns.
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from api.models import Item


@pytest.mark.django_db
class TestItemManager:
    """Test suite for ItemManager."""
    
    def test_completed_manager(self):
        """Test completed() manager method."""
        Item.objects.create(title="Completed 1", completed=True)
        Item.objects.create(title="Completed 2", completed=True)
        Item.objects.create(title="Pending 1", completed=False)
        
        completed = Item.objects.completed()
        assert completed.count() == 2
        assert all(item.completed for item in completed)
    
    def test_pending_manager(self):
        """Test pending() manager method."""
        Item.objects.create(title="Completed", completed=True)
        Item.objects.create(title="Pending 1", completed=False)
        Item.objects.create(title="Pending 2", completed=False)
        
        pending = Item.objects.pending()
        assert pending.count() == 2
        assert all(not item.completed for item in pending)
    
    def test_overdue_manager(self):
        """Test overdue() manager method."""
        Item.objects.create(
            title="Overdue",
            due_date=timezone.now() - timedelta(days=1),
            completed=False
        )
        Item.objects.create(
            title="Future",
            due_date=timezone.now() + timedelta(days=1),
            completed=False
        )
        Item.objects.create(
            title="Completed Overdue",
            due_date=timezone.now() - timedelta(days=1),
            completed=True
        )
        
        overdue = Item.objects.overdue()
        assert overdue.count() == 1
        assert overdue.first().title == "Overdue"
    
    def test_due_today_manager(self):
        """Test due_today() manager method."""
        today = timezone.now().date()
        Item.objects.create(
            title="Today",
            due_date=timezone.make_aware(
                timezone.datetime.combine(today, timezone.datetime.min.time())
            ),
            completed=False
        )
        Item.objects.create(
            title="Tomorrow",
            due_date=timezone.now() + timedelta(days=1),
            completed=False
        )
        
        due_today = Item.objects.due_today()
        assert due_today.count() == 1
        assert due_today.first().title == "Today"
    
    def test_search_manager(self):
        """Test search() manager method."""
        Item.objects.create(
            title="Python Developer",
            description="Looking for Python skills",
            tags="python, django"
        )
        Item.objects.create(
            title="JavaScript Developer",
            description="React and Vue.js",
            tags="javascript"
        )
        
        results = Item.objects.search("Python")
        assert results.count() == 1
        assert results.first().title == "Python Developer"
        
        results = Item.objects.search("django")
        assert results.count() == 1
    
    def test_high_priority_pending_manager(self):
        """Test high_priority_pending() manager method."""
        Item.objects.create(title="High", priority="high", completed=False)
        Item.objects.create(title="Urgent", priority="urgent", completed=False)
        Item.objects.create(title="Low", priority="low", completed=False)
        Item.objects.create(title="High Completed", priority="high", completed=True)
        
        high_priority = Item.objects.high_priority_pending()
        assert high_priority.count() == 2
        priorities = [item.priority for item in high_priority]
        assert "high" in priorities
        assert "urgent" in priorities
