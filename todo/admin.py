from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'completed', 'due_date', 'created_at')
    list_filter = ('completed', 'priority')
    search_fields = ('title', 'description')
    list_editable = ('completed', 'priority')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
