from django.urls import path
from . import views


urlpatterns = [
    path("daily-reset/", views.daily_reset, name="daily_reset"),
    path("strategies/", views.strategy_library, name="strategy_library"),
    path("strategies/search/", views.strategy_search, name="strategy_search"),
]