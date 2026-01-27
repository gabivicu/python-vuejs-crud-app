"""
Unit tests for ItemSerializer.
Demonstrates serializer validation and serialization testing.
"""
from datetime import timedelta

import pytest
from django.utils import timezone

from api.models import Item
from api.serializers import ItemSerializer


@pytest.mark.django_db
class TestItemSerializer:
    """Test suite for ItemSerializer."""

    def test_serialize_item(self):
        """Test serializing an item to JSON."""
        item = Item.objects.create(
            title="Test Item",
            description="Test description",
            category="work",
            priority="high",
            tags="tag1, tag2",
        )
        serializer = ItemSerializer(item)
        data = serializer.data

        assert data["title"] == "Test Item"
        assert data["description"] == "Test description"
        assert data["category"] == "work"
        assert data["priority"] == "high"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert data["tags_list"] == ["tag1", "tag2"]

    def test_deserialize_create_item(self):
        """Test creating an item from JSON data."""
        data = {
            "title": "New Item",
            "description": "New description",
            "category": "personal",
            "priority": "medium",
            "tags": "tag1, tag2, tag3",
        }
        serializer = ItemSerializer(data=data)
        assert serializer.is_valid()
        item = serializer.save()

        assert item.title == "New Item"
        assert item.description == "New description"
        assert item.category == "personal"
        assert item.priority == "medium"
        assert item.tags == "tag1, tag2, tag3"
        assert item.pk is not None

    def test_deserialize_create_item_missing_title(self):
        """Test validation error when title is missing on create."""
        data = {
            "description": "Description without title",
            "category": "work",
        }
        serializer = ItemSerializer(data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_deserialize_update_item(self):
        """Test updating an item with partial data."""
        item = Item.objects.create(
            title="Original Title",
            description="Original description",
            category="work",
            priority="low",
        )
        data = {"title": "Updated Title"}
        serializer = ItemSerializer(item, data=data, partial=True)
        assert serializer.is_valid()
        updated_item = serializer.save()

        assert updated_item.title == "Updated Title"
        assert updated_item.description == "Original description"
        assert updated_item.category == "work"

    def test_tags_list_field(self):
        """Test tags_list serialization."""
        item = Item.objects.create(
            title="Test",
            tags="tag1, tag2, tag3",
        )
        serializer = ItemSerializer(item)
        assert serializer.data["tags_list"] == ["tag1", "tag2", "tag3"]

    def test_tags_list_empty(self):
        """Test tags_list with empty tags."""
        item = Item.objects.create(title="Test", tags="")
        serializer = ItemSerializer(item)
        assert serializer.data["tags_list"] == []

    def test_tags_list_with_spaces(self):
        """Test tags_list with extra spaces."""
        item = Item.objects.create(title="Test", tags=" tag1 , tag2 , tag3 ")
        serializer = ItemSerializer(item)
        assert serializer.data["tags_list"] == ["tag1", "tag2", "tag3"]

    def test_read_only_fields(self):
        """Test that read-only fields cannot be set."""
        item = Item.objects.create(title="Test", tags="original, tags")
        original_id = item.id
        original_tags = item.tags
        data = {
            "id": 999,
            "created_at": timezone.now(),
            "updated_at": timezone.now(),
            "tags_list": ["custom", "tags"],
        }
        serializer = ItemSerializer(item, data=data, partial=True)
        assert serializer.is_valid()
        updated_item = serializer.save()

        # Read-only fields should not be changed
        assert updated_item.id == original_id  # ID should remain unchanged
        assert updated_item.tags == original_tags  # tags should remain unchanged
        # tags_list is computed from tags, so it should reflect original tags
        serializer_after = ItemSerializer(updated_item)
        assert serializer_after.data["tags_list"] == ["original", "tags"]

    def test_validate_all_fields(self):
        """Test validation with all fields."""
        data = {
            "title": "Complete Item",
            "description": "Full description",
            "category": "health",
            "priority": "urgent",
            "completed": True,
            "due_date": timezone.now() + timedelta(days=7),
            "tags": "important, urgent",
        }
        serializer = ItemSerializer(data=data)
        assert serializer.is_valid()
        item = serializer.save()

        assert item.title == "Complete Item"
        assert item.completed is True
        assert item.category == "health"
        assert item.priority == "urgent"
