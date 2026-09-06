import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from django.conf import settings

from .forms import DailyCheckInForm
from .models import Strategy
from tasks.models import Task

def AI_suggestion(check_in, tasks):
    if not settings.GROQ_API_KEY:
        return None
    
    task_info = "\n".join(f" - {t.title} (urgent: {t.urgent}, important: {t.important})" for t in tasks) or "No open Tasks."
    
    prompt = (
        "A neurodivergent student with ADHD just completed a daily check-in on their productivity app.\n"
        f"Energy: {check_in.get_energy_display()}\n"
        f"Mood: {check_in.get_mood_display()}\n"
        f"Note from them: {check_in.note or 'None'}\n\n"
        f"Open tasks in their list:\n{task_info}\n\n"
        "You do not know how long each task actually takes, so do not invent specific time estimates or a multi-step schedule. "
        "Reply with 2 to 4 short bullet points, each on its own line starting with '- '. "
        "The first bullet should name the ONE task from the list they should start with first today, and briefly say why, given their energy and mood. "
        "The other bullets can offer short, practical, encouraging tips for getting started, without specifying minutes. "
        "Plain text only, no headings, no markdown formatting other than the leading '- ' on each line."
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

            recommended_strategy = Strategy.objects.filter(active=True, energy_level__in=[check_in.energy, "any"]).first()
            
            open_tasks= Task.objects.filter(user=request.user, completed=False)
            ai_suggestion_text = AI_suggestion(check_in, open_tasks)
            ai_suggestion = []
            if ai_suggestion_text:
                for line in ai_suggestion_text.split("\n"):
                    line = line.strip().lstrip("-").strip()
                    if line:
                        ai_suggestion.append(line)            
            
            return render(request, "wellbeing/daily_reset_result.html", {"check_in": check_in, "mode": mode, "message": message, "recommended_strategy": recommended_strategy, "ai_suggestion": ai_suggestion,})

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

