import random
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.conf import settings
from django.utils import timezone

from .forms import DailyCheckInForm, RoutineForm, JournalEntryForm
from .models import Strategy, Routine, RoutineStep, DopamineMenuItem, JournalEntry
from tasks.models import Task

def AI_suggestion(check_in, tasks, routines):
    if not settings.GROQ_API_KEY:
        return None
    
    task_info = "\n".join(f" - {t.title} (urgent: {t.urgent}, important: {t.important})" for t in tasks) or "No open Tasks."
    routine_info = "\n".join(f"- {r.title}: {r.description}" for r in routines) or "No matching routines right now."
    
    prompt = (
        "A neurodivergent student with ADHD just completed a daily check-in on their productivity app.\n"
        f"Energy: {check_in.get_energy_display()}\n"
        f"Mood: {check_in.get_mood_display()}\n"
        f"Note from them: {check_in.note or 'None'}\n\n"
        f"Open tasks in their list:\n{task_info}\n\n"
        f"Routines available that match today's mode:\n{routine_info}\n\n"
        "You do not know how long each task actually takes, so do not invent specific time estimates or a multi-step schedule. "
        "Reply with 2 to 4 short bullet points, each on its own line starting with '- '. "
        "The first bullet should name the ONE task from the list they should start with first today, and briefly say why, given their energy and mood. "
        "The other bullets can offer short, practical, encouraging tips for getting started, without specifying minutes. "
        "If one of the available routines would genuinely help them today, mention it by name in one of the bullets. "
        "Plain text only. Do not use asterisks, bold, italics, headings, or any markdown formatting other than the leading '- ' on each line."
    )
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [{"role": "user", "content":prompt}],
                "reasoning_effort": "low",
                "max_tokens":600,
            },
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("AI suggestion failed:", e)
        return None

@login_required
def daily_reset(request):
    if request.method == "POST":
        form = DailyCheckInForm(request.POST)
        if form.is_valid():
            check_in = form.save(commit=False)
            check_in.user = request.user
            check_in.save()
            
            if check_in.energy == "low":
                if check_in.mood in ["overwhelmed", "stressed"]:
                    mode = "Recovery Mode"
                    message = "Today is about reducing pressure and focusing only on what really matters."
                else:
                    mode = "Low-Energy Mode"
                    message = "Keep today simple. Focus on essential tasks and small achievable steps."
            elif check_in.energy == "medium":
                if check_in.mood in ["stressed", "overwhelmed"]:
                    mode = "Steady Mode"
                    message = "You have some capacity, but today needs structure without too much pressure."
                else:
                    mode= "Balanced Mode"
                    message="You have enough capacity for a balanced day. Choose a few meaningful priorities"
            else:
                if check_in.mood == "motivated":
                    mode = "Progress Mode"
                    message = "You have good capacity and momentum. This is a good time to tackle something meaningful."
                else:
                    mode = "Balanced Mode"
                    message = "You have good capacity today. Make progress while keeping your workload realistic."
            
            mode_key_map = {
                "Recovery Mode": "recovery",
                "Low-Energy Mode": "low_energy",
                "Steady Mode": "steady",
                "Balanced Mode": "balanced",
                "Progress Mode": "progress",
            }
            mode_key = mode_key_map.get(mode)

            open_tasks = Task.objects.filter(user=request.user, completed=False)
            has_urgent_important = open_tasks.filter(urgent=True, important=True).exists()

            matching_routines = Routine.objects.filter(active=True, mode=mode_key).filter(
                Q(created_by__isnull=True) | Q(created_by=request.user)
            )

            current_hour = timezone.now().hour
            if 5 <= current_hour < 12:
                matching_routines = matching_routines.exclude(routine_type="evening")
            elif 12 <= current_hour < 18:
                matching_routines = matching_routines.exclude(routine_type__in=["morning", "evening"])
            else:
                matching_routines = matching_routines.exclude(routine_type="morning")

            if has_urgent_important and check_in.energy == "low":
                matching_routines = matching_routines.exclude(routine_type__in=["cleaning", "cooking"])

            recommended_routine = matching_routines.first()
            
            recommended_strategies = Strategy.objects.filter(active=True, energy_level__in=[check_in.energy, "any"]).order_by("category")[:3]
            
            ai_suggestion_text = AI_suggestion(check_in, open_tasks, matching_routines)
            ai_suggestion = []
            if ai_suggestion_text:
                for line in ai_suggestion_text.split("\n"):
                    line = line.strip().lstrip("-").strip()
                    line = line.replace("*", "")
                    if line:
                        ai_suggestion.append(line)            
            
            response = render(request, "wellbeing/daily_reset_result.html", {"check_in": check_in, "mode": mode, "message": message, "recommended_strategies": recommended_strategies, "ai_suggestion": ai_suggestion, "recommended_routine": recommended_routine,})
            response.set_cookie("last_reset_mode", mode, max_age=60 * 60 * 24 * 7)
            return response
    else:
        form = DailyCheckInForm()
    return render(request, "wellbeing/daily_reset.html", {"form": form,})

@login_required
def strategy_library(request):
    strategies = Strategy.objects.filter(active=True).order_by("category", "title")
    return render(request, "wellbeing/strategy_library.html", {"strategies": strategies})
    
@login_required
def strategy_search(request):
    query = request.GET.get("q", "")
    strategies = Strategy.objects.filter(active=True)
    if query:
        strategies = strategies.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    return render(request, "wellbeing/_strategy_cards.html", {"strategies": strategies})

@login_required
def routine_list(request):
    routines = Routine.objects.filter(active=True).filter(
        Q(created_by__isnull=True) | Q(created_by=request.user)
    ).prefetch_related("steps").order_by("routine_type", "title")
    routine_id = request.GET.get("routine")
    if routine_id:
        routines = routines.filter(id=routine_id)
    return render(request, "wellbeing/routine_list.html", {"routines": routines})

@login_required
def routine_search(request):
    query = request.GET.get("q", "")
    routines = Routine.objects.filter(active=True).filter(
        Q(created_by__isnull=True) | Q(created_by=request.user)
    ).prefetch_related("steps")
    if query:
        routines = routines.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    routines = routines.order_by("routine_type", "title")
    return render(request, "wellbeing/_routine_cards.html", {"routines": routines})

@login_required
def add_routine(request):
    if request.method == "POST":
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.created_by = request.user
            routine.save()
            steps_text = form.cleaned_data.get("steps_text", "")
            for index, line in enumerate(steps_text.splitlines(), start=1):
                line = line.strip()
                if line:
                    RoutineStep.objects.create(routine=routine, title=line, order=index)
            return redirect("routine_list")
    else:
        form = RoutineForm()
    return render(request, "wellbeing/add_routine.html", {"form": form})

@login_required
def dashboard(request):
    open_tasks = Task.objects.filter(user=request.user, completed=False)
    priority_tasks = open_tasks.filter(urgent=True, important=True).order_by("-created_at")[:5]
    my_tasks = open_tasks.filter(ai_generated=False).order_by("-created_at")
    ai_tasks = open_tasks.filter(ai_generated=True).order_by("-created_at")
    last_reset_mode = request.COOKIES.get("last_reset_mode")

    dopamine_items = list(DopamineMenuItem.objects.filter(active=True))
    dopamine_suggestion = random.choice(dopamine_items) if dopamine_items else None

    return render(request, "wellbeing/dashboard.html", {
        "my_tasks": my_tasks,
        "ai_tasks": ai_tasks,
        "priority_tasks": priority_tasks,
        "last_reset_mode": last_reset_mode,
        "dopamine_suggestion": dopamine_suggestion,
    })

@login_required
def dopamine_menu(request):
    items = DopamineMenuItem.objects.filter(active=True)

    grouped = []
    for key, label in DopamineMenuItem.CATEGORY_CHOICES:
        category_items = items.filter(category=key)
        if category_items.exists():
            grouped.append({"label": label, "items": category_items})

    return render(request, "wellbeing/dopamine_menu.html", {"grouped": grouped})

@login_required
def edit_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id, created_by=request.user)

    if request.method == "POST":
        form = RoutineForm(request.POST, instance=routine)
        if form.is_valid():
            form.save()
            routine.steps.all().delete()
            steps_text = form.cleaned_data.get("steps_text", "")
            for index, line in enumerate(steps_text.splitlines(), start=1):
                line = line.strip()
                if line:
                    RoutineStep.objects.create(routine=routine, title=line, order=index)
            return redirect("routine_list")
    else:
        existing_steps = "\n".join(step.title for step in routine.steps.all())
        form = RoutineForm(instance=routine, initial={"steps_text": existing_steps})

    return render(request, "wellbeing/edit_routine.html", {"form": form, "routine": routine})

@login_required
def delete_routine(request, routine_id):
    routine = get_object_or_404(Routine, id=routine_id, created_by=request.user)
    if request.method == "POST":
        routine.delete()
        return redirect("routine_list")
    return render(request, "wellbeing/delete_routine.html", {"routine": routine})

@login_required
def journal_list(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect("journal_list")
    else:
        form = JournalEntryForm()

    entries = JournalEntry.objects.filter(user=request.user)
    return render(request, "wellbeing/journal_list.html", {"form": form, "entries": entries})

@login_required
def edit_journal_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("journal_list")
    else:
        form = JournalEntryForm(instance=entry)
    return render(request, "wellbeing/edit_journal_entry.html", {"form": form, "entry": entry})

@login_required
def delete_journal_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        entry.delete()
        return redirect("journal_list")
    return render(request, "wellbeing/delete_journal_entry.html", {"entry": entry})