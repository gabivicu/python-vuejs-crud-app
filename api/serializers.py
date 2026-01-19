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

    def get_tags_list(self, obj):
        """Return tags as a list."""
        return obj.get_tags_list()
