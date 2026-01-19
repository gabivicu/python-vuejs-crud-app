"""
Unit tests for Item model.
Demonstrates comprehensive testing practices.
"""
from datetime import timedelta

import pytest
from django.utils import timezone

from api.models import Item


@pytest.mark.django_db
class TestItemModel:
    """Test suite for Item model."""

    def test_item_creation(self):
        """Test basic item creation."""
        item = Item.objects.create(
            title="Test Item",
            description="Test description",
            category="work",
            priority="high",
        )
        assert item.title == "Test Item"
        assert item.completed is False
        assert item.category == "work"
        assert item.priority == "high"
        assert item.pk is not None

    def test_get_tags_list(self):
        """Test tag parsing."""
        item = Item.objects.create(title="Test", tags="tag1, tag2, tag3")
        tags = item.get_tags_list()
        assert len(tags) == 3
        assert "tag1" in tags
        assert "tag2" in tags
        assert "tag3" in tags

    def test_is_overdue(self):
        """Test overdue detection."""
        # Overdue item
        overdue_item = Item.objects.create(
            title="Overdue",
            due_date=timezone.now() - timedelta(days=1),
            completed=False,
        )
        assert overdue_item.is_overdue() is True

        # Not overdue (future date)
        future_item = Item.objects.create(
            title="Future", due_date=timezone.now() + timedelta(days=1), completed=False
        )
        assert future_item.is_overdue() is False

        # Completed item is never overdue
        completed_item = Item.objects.create(
            title="Completed",
            due_date=timezone.now() - timedelta(days=1),
            completed=True,
        )
        assert completed_item.is_overdue() is False

    def test_mark_complete(self):
        """Test marking item as complete."""
        item = Item.objects.create(title="Test", completed=False)
        item.mark_complete()
        item.refresh_from_db()
        assert item.completed is True

    def test_mark_pending(self):
        """Test marking item as pending."""
        item = Item.objects.create(title="Test", completed=True)
        item.mark_pending()
        item.refresh_from_db()
        assert item.completed is False
