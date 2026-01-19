from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'completed', 'due_date', 'created_at', 'updated_at']
    list_filter = ['completed', 'category', 'priority', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'tags']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

