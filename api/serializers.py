from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()

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
            "due_date": {"required": False},
            "tags": {"required": False},
        }

    def get_tags_list(self, obj):
        """Return tags as a list."""
        return obj.get_tags_list()

    def validate(self, attrs):
        """Validate that title is provided on create, but optional on update."""
        # On create (no instance), title is required
        if self.instance is None and "title" not in attrs:
            raise serializers.ValidationError({"title": "This field is required."})
        return attrs
