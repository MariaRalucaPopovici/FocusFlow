from django.urls import path
from . import views


urlpatterns = [
    path("daily-reset/", views.daily_reset, name="daily_reset"),
]