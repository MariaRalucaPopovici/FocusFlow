from django.contrib import admin
from django.urls import path, include
from tasks.views import TaskListCreateAPI, TaskDetailAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("tasks/", include("tasks.urls")),
    path("wellbeing/", include("wellbeing.urls")),
    path("",include("tasks.urls")),
    path("api/tasks/", TaskListCreateAPI.as_view(), name="api_task_list"),
    path("api/tasks/<int:pk>/", TaskDetailAPI.as_view(), name="api_task_detail"),
]
