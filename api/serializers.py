from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "category",
            "priority",
            "due_date",
            "tags",
            "tags_list",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "tags_list"]
        # Allow partial updates (PATCH) without requiring all fields
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "category": {"required": False},
            "priority": {"required": False},
            "tags": {"required": False},
        }

    def get_tags_list(self, obj):
        """Return tags as a list."""
        return obj.get_tags_list()

    def validate_due_date(self, value):
        """Convert date string to datetime if needed."""
        if value is None or value == "":
            return None

        # If value is already a datetime, return it
        if isinstance(value, datetime):
            return value

        # If value is a string, try to parse it
        if isinstance(value, str):
            # Remove whitespace
            value = value.strip()
            if not value:
                return None

            # Try parsing as date (YYYY-MM-DD)
            try:
                date_obj = datetime.strptime(value, "%Y-%m-%d")
                # Set time to end of day (23:59:59)
                return timezone.make_aware(
                    datetime.combine(date_obj.date(), datetime.max.time())
                )
            except ValueError:
                # If it's not a date format, let Django REST Framework handle it
                # It will raise its own validation error if format is wrong
                pass

        return value

    def validate(self, attrs):
        """Validate that title is provided on create, but optional on update."""
        # On create (no instance), title is required
        if self.instance is None and "title" not in attrs:
            raise serializers.ValidationError({"title": "This field is required."})
        return attrs
