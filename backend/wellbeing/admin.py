from django.contrib import admin
from .models import DailyCheckIn, Strategy, Routine, RoutineStep, DopamineMenuItem

@admin.register(DailyCheckIn)
class DailyCheckInAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "energy",
        "mood",
    )

    list_filter = (
        "energy",
        "date",
    )

    search_fields = (
        "user__username",
        "mood",
        "note",
    )

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = (
        "title", 
        "category",
        "energy_level",
        "duration_minutes",
        "active",
    )
    
    list_filter = (
        "category",
        "energy_level",
        "active",
    )
    
    search_fields = (
        "title",
        "description",
    )
    
class RoutineStepInline(admin.TabularInline):
    model = RoutineStep
    extra = 1
    
@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "routine_type",
        "mode",
        "active",
    )
    
    list_filter = (
        "routine_type",
        "mode",
        "active",
    )
    
    inlines = [
        RoutineStepInline
    ]

@admin.register(RoutineStep)
class RoutineStepAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "routine",
        "order",
        "duration_minutes",
        "strategy",
    )

@admin.register(DopamineMenuItem)
class DopamineMenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "active",
    )

    list_filter = (
        "category",
        "active",
    )