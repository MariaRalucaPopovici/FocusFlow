from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "deadline",
        "urgent",
        "important",
        "completed",
        "created_at",
    )
    
    list_filter = (
        "completed",
        "urgent",
        "important",
    )
    
    search_fields = (
        "title",
        "description",
        "user__username",
    )
