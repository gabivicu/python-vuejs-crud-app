from django.db import models
from django.utils import timezone

from .managers import ItemManager


class Item(models.Model):
    """
    Model representing an item in the CRUD app.

    Features:
    - Custom managers and querysets
    - Database indexing for performance
    - Model methods for business logic
    """

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    CATEGORY_CHOICES = [
        ("work", "Work"),
        ("personal", "Personal"),
        ("shopping", "Shopping"),
        ("health", "Health"),
        ("finance", "Finance"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False, db_index=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other", db_index=True
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium", db_index=True
    )
    due_date = models.DateTimeField(null=True, blank=True, db_index=True)
    tags = models.CharField(
        max_length=500, blank=True, help_text="Comma-separated tags"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Custom manager
    objects = ItemManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["completed", "priority"]),
            models.Index(fields=["category", "completed"]),
            models.Index(fields=["due_date", "completed"]),
            models.Index(fields=["-created_at"]),
        ]
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.title

    def get_tags_list(self):
        """Return tags as a list."""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
        return []

    def is_overdue(self):
        """Check if item is overdue."""
        if not self.due_date or self.completed:
            return False
        return self.due_date < timezone.now()

    def days_until_due(self):
        """Calculate days until due date."""
        if not self.due_date:
            return None
        delta = self.due_date - timezone.now()
        return delta.days

    def mark_complete(self):
        """Mark item as complete."""
        self.completed = True
        self.save(update_fields=["completed", "updated_at"])

    def mark_pending(self):
        """Mark item as pending."""
        self.completed = False
        self.save(update_fields=["completed", "updated_at"])
