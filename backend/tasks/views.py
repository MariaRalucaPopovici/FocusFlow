from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
import requests
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
    
def generate_tasks_from_text(description):
    if not settings.GROQ_API_KEY:
        return None

    prompt = (
        "A user of an ADHD productivity app described a task or goal they need to get done.\n"
        f"Their description: {description}\n\n"
        "Break this down into no more than 4 small, specific, actionable to-do items that together would accomplish it. "
        "Do not create more than 4 items under any circumstances, even if the task seems big - keep items broad enough to stay within that limit. "
        "Each item should be short (under 12 words), start with a verb, and be concrete enough to start immediately - "
        "avoid vague items like 'work on it' or 'plan the project'. "
        "For each item, also decide whether it is URGENT (needs attention very soon) and whether it is IMPORTANT "
        "(has real consequences if not done), based on the user's description. "
        "Reply with ONLY the list, one item per line, in EXACTLY this format with no extra text:\n"
        "TITLE | URGENT_YES_OR_NO | IMPORTANT_YES_OR_NO\n"
        "For example:\n"
        "Book the dentist appointment | yes | yes\n"
        "Tidy the desk surface | no | no\n"
        "Do not include headings, numbering, bullet points, or any markdown formatting - just the plain lines above."
    )

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [{"role": "user", "content": prompt}],
                "reasoning_effort": "low",
                "max_tokens": 400,
            },
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("AI task generation failed:", e)
        return None

@login_required
def ai_generate_tasks(request):
    if request.method == "POST":
        description = request.POST.get("description", "").strip()
        next_url = request.POST.get("next") or "task_list"

        if not description:
            messages.error(request, "Please describe what you need to get done.")
            return redirect("ai_generate_tasks")

        result_text = generate_tasks_from_text(description)

        if not result_text:
            messages.error(request, "AI task generation isn't available right now. Please try again later, or add tasks manually.")
            return redirect("ai_generate_tasks")

        created_count = 0
        for line in result_text.split("\n"):
            if created_count >= 4:
                break
            line = line.strip().lstrip("-").strip()
            line = line.replace("*", "")
            if not line:
                continue

            parts = line.split("|")
            title = parts[0].strip()
            urgent = len(parts) > 1 and parts[1].strip().lower().startswith("y")
            important = len(parts) > 2 and parts[2].strip().lower().startswith("y")

            if title:
                Task.objects.create(
                    user=request.user,
                    title=title[:200],
                    urgent=urgent,
                    important=important,
                    ai_generated=True,
                )
                created_count += 1

        if created_count:
            messages.success(request, f"Added {created_count} new task{'s' if created_count != 1 else ''} to your list.")
        else:
            messages.error(request, "Something went wrong generating tasks. Please try again.")

        return redirect(next_url)

    return render(request, "tasks/ai_generate_tasks.html")