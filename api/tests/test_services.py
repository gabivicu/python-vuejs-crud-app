"""
Unit tests for ItemService.
Demonstrates service layer testing and caching behavior.
"""
from datetime import timedelta

import pytest
from django.core.cache import cache
from django.utils import timezone

from api.models import Item
from api.services import ItemService


@pytest.mark.django_db
class TestItemService:
    """Test suite for ItemService."""

    def setup_method(self):
        """Clear cache before each test."""
        cache.clear()

    def test_get_statistics_empty(self):
        """Test statistics with no items."""
        stats = ItemService.get_statistics()

        assert stats["total"] == 0
        assert stats["completed"] == 0
        assert stats["pending"] == 0
        assert stats["overdue"] == 0
        assert stats["due_today"] == 0
        assert stats["high_priority_pending"] == 0
        assert stats["completion_rate"] == 0
        assert isinstance(stats["priority_stats"], dict)
        assert isinstance(stats["category_stats"], dict)

    def test_get_statistics_with_items(self):
        """Test statistics with various items."""
        # Create test items
        Item.objects.create(title="Completed 1", completed=True, priority="high")
        Item.objects.create(title="Completed 2", completed=True, priority="low")
        Item.objects.create(title="Pending 1", completed=False, priority="high")
        Item.objects.create(
            title="Overdue",
            completed=False,
            due_date=timezone.now() - timedelta(days=1),
        )
        # Create item due today (use future time to ensure it's not overdue)
        # Add 1 hour to current time to ensure it's in the future
        # This ensures it's still "due today" but not overdue
        Item.objects.create(
            title="Due Today",
            completed=False,
            due_date=timezone.now() + timedelta(hours=1),
        )

        stats = ItemService.get_statistics()

        assert stats["total"] == 5
        assert stats["completed"] == 2
        assert stats["pending"] == 3
        assert stats["overdue"] == 1
        assert stats["due_today"] == 1
        assert stats["high_priority_pending"] == 1
        assert stats["completion_rate"] == 40.0

    def test_get_statistics_caching(self):
        """Test that statistics are cached."""
        Item.objects.create(title="Test", completed=True)

        # First call - should compute
        stats1 = ItemService.get_statistics()
        assert stats1["total"] == 1

        # Create another item but don't invalidate cache
        Item.objects.create(title="Test 2", completed=False)

        # Second call - should return cached data
        stats2 = ItemService.get_statistics()
        assert stats2["total"] == 1  # Still shows old count

        # Invalidate cache
        ItemService.invalidate_statistics_cache()

        # Third call - should recompute
        stats3 = ItemService.get_statistics()
        assert stats3["total"] == 2

    def test_invalidate_statistics_cache(self):
        """Test cache invalidation."""
        Item.objects.create(title="Test")
        ItemService.get_statistics()  # Populate cache

        # Verify cache exists
        assert cache.get("item_statistics") is not None

        # Invalidate
        ItemService.invalidate_statistics_cache()

        # Verify cache is cleared
        assert cache.get("item_statistics") is None

    def test_search_items_with_query(self):
        """Test search_items with search query."""
        Item.objects.create(title="Python Developer", description="Python skills")
        Item.objects.create(title="JavaScript Developer", description="JS skills")
        Item.objects.create(title="Python Expert", tags="python, django")

        results = ItemService.search_items("Python")
        assert results.count() == 2

    def test_search_items_without_query(self):
        """Test search_items without query returns all."""
        Item.objects.create(title="Item 1")
        Item.objects.create(title="Item 2")
        Item.objects.create(title="Item 3")

        results = ItemService.search_items("")
        assert results.count() == 3

    def test_search_items_with_category_filter(self):
        """Test search_items with category filter."""
        Item.objects.create(title="Work Item", category="work")
        Item.objects.create(title="Personal Item", category="personal")
        Item.objects.create(title="Another Work Item", category="work")

        results = ItemService.search_items("", filters={"category": "work"})
        assert results.count() == 2
        assert all(item.category == "work" for item in results)

    def test_search_items_with_priority_filter(self):
        """Test search_items with priority filter."""
        Item.objects.create(title="High Priority", priority="high")
        Item.objects.create(title="Low Priority", priority="low")
        Item.objects.create(title="Another High", priority="high")

        results = ItemService.search_items("", filters={"priority": "high"})
        assert results.count() == 2
        assert all(item.priority == "high" for item in results)

    def test_search_items_with_completed_filter(self):
        """Test search_items with completed filter."""
        Item.objects.create(title="Completed", completed=True)
        Item.objects.create(title="Pending 1", completed=False)
        Item.objects.create(title="Pending 2", completed=False)

        results = ItemService.search_items("", filters={"completed": True})
        assert results.count() == 1
        assert all(item.completed for item in results)

        results = ItemService.search_items("", filters={"completed": False})
        assert results.count() == 2
        assert all(not item.completed for item in results)

    def test_search_items_with_overdue_filter(self):
        """Test search_items with overdue filter."""
        Item.objects.create(
            title="Overdue",
            completed=False,
            due_date=timezone.now() - timedelta(days=1),
        )
        Item.objects.create(
            title="Future",
            completed=False,
            due_date=timezone.now() + timedelta(days=1),
        )
        Item.objects.create(
            title="Completed Overdue",
            completed=True,
            due_date=timezone.now() - timedelta(days=1),
        )

        results = ItemService.search_items("", filters={"due_filter": "overdue"})
        assert results.count() == 1
        assert results.first().title == "Overdue"

    def test_search_items_with_today_filter(self):
        """Test search_items with today filter."""
        today = timezone.now()
        Item.objects.create(
            title="Due Today",
            completed=False,
            due_date=today,
        )
        Item.objects.create(
            title="Due Tomorrow",
            completed=False,
            due_date=today + timedelta(days=1),
        )

        results = ItemService.search_items("", filters={"due_filter": "today"})
        assert results.count() == 1
        assert results.first().title == "Due Today"

    def test_search_items_with_multiple_filters(self):
        """Test search_items with multiple filters combined."""
        Item.objects.create(
            title="High Work Item",
            category="work",
            priority="high",
            completed=False,
        )
        Item.objects.create(
            title="High Personal Item",
            category="personal",
            priority="high",
            completed=False,
        )
        Item.objects.create(
            title="Low Work Item",
            category="work",
            priority="low",
            completed=False,
        )

        results = ItemService.search_items(
            "", filters={"category": "work", "priority": "high"}
        )
        assert results.count() == 1
        assert results.first().title == "High Work Item"

    def test_bulk_update_status(self):
        """Test bulk_update_status."""
        item1 = Item.objects.create(title="Item 1", completed=False)
        item2 = Item.objects.create(title="Item 2", completed=False)
        item3 = Item.objects.create(title="Item 3", completed=False)

        updated = ItemService.bulk_update_status([item1.id, item2.id], True)

        assert updated == 2
        item1.refresh_from_db()
        item2.refresh_from_db()
        item3.refresh_from_db()
        assert item1.completed is True
        assert item2.completed is True
        assert item3.completed is False

    def test_bulk_update_status_invalidates_cache(self):
        """Test that bulk_update_status invalidates cache."""
        Item.objects.create(title="Test", completed=False)
        ItemService.get_statistics()  # Populate cache

        assert cache.get("item_statistics") is not None

        ItemService.bulk_update_status([Item.objects.first().id], True)

        # Cache should be invalidated
        assert cache.get("item_statistics") is None

    def test_bulk_delete(self):
        """Test bulk_delete."""
        item1 = Item.objects.create(title="Item 1")
        item2 = Item.objects.create(title="Item 2")
        item3 = Item.objects.create(title="Item 3")

        deleted = ItemService.bulk_delete([item1.id, item2.id])

        assert deleted == 2
        assert not Item.objects.filter(id=item1.id).exists()
        assert not Item.objects.filter(id=item2.id).exists()
        assert Item.objects.filter(id=item3.id).exists()

    def test_bulk_delete_invalidates_cache(self):
        """Test that bulk_delete invalidates cache."""
        item = Item.objects.create(title="Test")
        ItemService.get_statistics()  # Populate cache

        assert cache.get("item_statistics") is not None

        ItemService.bulk_delete([item.id])

        # Cache should be invalidated
        assert cache.get("item_statistics") is None
