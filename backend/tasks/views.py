from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import generics, permissions
from .serializers import TaskSerializer

@login_required
def task_list(request):
    
    tasks = Task.objects.filter(user=request.user)
    last_reset_mode = request.COOKIES.get("last_reset_mode")
    
    return render(request, "tasks/task_list.html", {"tasks": tasks, "last_reset_mode": last_reset_mode})

@login_required
def task_search(request):
    query = request.GET.get("q", "")
    tasks = Task.objects.filter(user=request.user)
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, "tasks/_task_cards.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/add_task.html", {"form":form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    
    return render(request, "tasks/edit_task.html", {"form":form, "task":task})

@login_required
def toggle_complete(request, task_id):
    
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    
    return redirect("task_list")

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "tasks/delete_task.html", {"task":task})

class TaskListCreateAPI(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
