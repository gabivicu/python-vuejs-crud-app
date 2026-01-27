"""
Integration tests for API views.
Demonstrates API testing best practices.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Item


@pytest.mark.django_db
class TestItemViewSet:
    """Test suite for ItemViewSet."""

    @pytest.fixture
    def client(self):
        """API client fixture."""
        return APIClient()

    @pytest.fixture
    def sample_items(self):
        """Create sample items for testing."""
        items = [
            Item.objects.create(
                title=f"Item {i}",
                description=f"Description {i}",
                category="work" if i % 2 == 0 else "personal",
                priority="high" if i < 3 else "low",
                completed=i < 2,
            )
            for i in range(5)
        ]
        return items

    def test_list_items(self, client, sample_items):
        """Test listing all items."""
        url = reverse("item-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data or isinstance(response.data, list)

    def test_create_item(self, client):
        """Test creating a new item."""
        url = reverse("item-list")
        data = {
            "title": "New Item",
            "description": "New description",
            "category": "work",
            "priority": "high",
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Item"
        assert Item.objects.filter(title="New Item").exists()

    def test_filter_by_category(self, client, sample_items):
        """Test filtering by category."""
        url = reverse("item-list")
        response = client.get(url, {"category": "work"})

        assert response.status_code == status.HTTP_200_OK
        # Verify all returned items are work category
        items = response.data.get("results", response.data)
        assert all(item["category"] == "work" for item in items)

    def test_filter_by_priority(self, client, sample_items):
        """Test filtering by priority."""
        url = reverse("item-list")
        response = client.get(url, {"priority": "high"})

        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        assert all(item["priority"] == "high" for item in items)

    def test_search(self, client, sample_items):
        """Test search functionality."""
        url = reverse("item-list")
        response = client.get(url, {"search": "Item 1"})

        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        assert len(items) > 0

    def test_stats_endpoint(self, client, sample_items):
        """Test stats endpoint."""
        url = reverse("item-stats")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "total" in response.data
        assert "completed" in response.data
        assert "pending" in response.data
        assert "priority_stats" in response.data
        assert "category_stats" in response.data

    def test_update_item(self, client, sample_items):
        """Test updating an item."""
        item = sample_items[0]
        url = reverse("item-detail", kwargs={"pk": item.pk})
        data = {
            "title": "Updated Title",
            "description": item.description,
            "category": item.category,
            "priority": item.priority,
            "completed": item.completed,
        }
        response = client.put(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Updated Title"
        item.refresh_from_db()
        assert item.title == "Updated Title"

    def test_delete_item(self, client, sample_items):
        """Test deleting an item."""
        item = sample_items[0]
        url = reverse("item-detail", kwargs={"pk": item.pk})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Item.objects.filter(pk=item.pk).exists()

    def test_partial_update_item(self, client, sample_items):
        """Test partial update (PATCH) of an item."""
        item = sample_items[0]
        url = reverse("item-detail", kwargs={"pk": item.pk})
        data = {"title": "Patched Title"}
        response = client.patch(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == "Patched Title"
        item.refresh_from_db()
        assert item.title == "Patched Title"

    def test_filter_by_completed(self, client, sample_items):
        """Test filtering by completion status."""
        url = reverse("item-list")
        response = client.get(url, {"completed": "true"})

        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        assert all(item["completed"] is True for item in items)

        response = client.get(url, {"completed": "false"})
        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        assert all(item["completed"] is False for item in items)

    def test_filter_by_due_overdue(self, client):
        """Test filtering by overdue items."""
        from datetime import timedelta

        from django.utils import timezone

        Item.objects.create(
            title="Overdue",
            due_date=timezone.now() - timedelta(days=1),
            completed=False,
        )
        Item.objects.create(
            title="Future",
            due_date=timezone.now() + timedelta(days=1),
            completed=False,
        )

        url = reverse("item-list")
        response = client.get(url, {"due_filter": "overdue"})

        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        assert len(items) == 1
        assert items[0]["title"] == "Overdue"

    def test_filter_by_due_today(self, client):
        """Test filtering by items due today."""
        from datetime import timedelta

        from django.utils import timezone

        today = timezone.now()
        Item.objects.create(
            title="Due Today",
            due_date=today,
            completed=False,
        )
        Item.objects.create(
            title="Due Tomorrow",
            due_date=today + timedelta(days=1),
            completed=False,
        )

        url = reverse("item-list")
        response = client.get(url, {"due_filter": "today"})

        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        assert len(items) == 1
        assert items[0]["title"] == "Due Today"

    def test_ordering(self, client, sample_items):
        """Test ordering of items."""
        url = reverse("item-list")
        response = client.get(url, {"ordering": "title"})

        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        titles = [item["title"] for item in items]
        assert titles == sorted(titles)

        response = client.get(url, {"ordering": "-title"})
        assert response.status_code == status.HTTP_200_OK
        items = response.data.get("results", response.data)
        titles = [item["title"] for item in items]
        assert titles == sorted(titles, reverse=True)

    def test_high_priority_pending_endpoint(self, client):
        """Test high_priority_pending endpoint."""
        Item.objects.create(title="High", priority="high", completed=False)
        Item.objects.create(title="Urgent", priority="urgent", completed=False)
        Item.objects.create(title="Low", priority="low", completed=False)
        Item.objects.create(title="High Completed", priority="high", completed=True)

        url = reverse("item-high-priority-pending")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        items = response.data
        assert len(items) == 2
        priorities = [item["priority"] for item in items]
        assert "high" in priorities
        assert "urgent" in priorities

    def test_retrieve_item(self, client, sample_items):
        """Test retrieving a single item."""
        item = sample_items[0]
        url = reverse("item-detail", kwargs={"pk": item.pk})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == item.pk
        assert response.data["title"] == item.title

    def test_retrieve_nonexistent_item(self, client):
        """Test retrieving a non-existent item."""
        url = reverse("item-detail", kwargs={"pk": 99999})
        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_item_with_all_fields(self, client):
        """Test creating item with all optional fields."""
        from datetime import timedelta

        from django.utils import timezone

        url = reverse("item-list")
        data = {
            "title": "Complete Item",
            "description": "Full description",
            "category": "health",
            "priority": "urgent",
            "completed": True,
            "due_date": (timezone.now() + timedelta(days=7)).isoformat(),
            "tags": "important, urgent",
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Complete Item"
        assert response.data["category"] == "health"
        assert response.data["priority"] == "urgent"
        assert response.data["completed"] is True
