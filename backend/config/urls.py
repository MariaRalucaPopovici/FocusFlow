from django.contrib import admin
from django.urls import path, include
from tasks.views import TaskListCreateAPI, TaskDetailAPI
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from wellbeing.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("tasks/", include("tasks.urls")),
    path("wellbeing/", include("wellbeing.urls")),
    path("", dashboard, name="home"),
    path("api/tasks/", TaskListCreateAPI.as_view(), name="api_task_list"),
    path("api/tasks/<int:pk>/", TaskDetailAPI.as_view(), name="api_task_detail"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
