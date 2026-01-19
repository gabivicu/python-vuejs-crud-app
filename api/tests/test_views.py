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
