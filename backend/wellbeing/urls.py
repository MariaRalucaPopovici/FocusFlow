from django.urls import path
from . import views


urlpatterns = [
    path("daily-reset/", views.daily_reset, name="daily_reset"),
    path("strategies/", views.strategy_library, name="strategy_library"),
    path("strategies/search/", views.strategy_search, name="strategy_search"),
    path("routines/", views.routine_list, name="routine_list"),
    path("routines/add/", views.add_routine, name="add_routine"),
    path("routines/search/", views.routine_search, name="routine_search"),
    path("routines/<int:routine_id>/edit/", views.edit_routine, name="edit_routine"),
    path("routines/<int:routine_id>/delete/", views.delete_routine, name="delete_routine"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dopamine-menu/", views.dopamine_menu, name="dopamine_menu"),
    path("journal/", views.journal_list, name="journal_list"),
    path("journal/<int:entry_id>/edit/", views.edit_journal_entry, name="edit_journal_entry"),
    path("journal/<int:entry_id>/delete/", views.delete_journal_entry, name="delete_journal_entry"),
]