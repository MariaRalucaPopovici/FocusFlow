from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import DailyCheckInForm
from .models import Strategy

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
            return render(request, "wellbeing/daily_reset.html", {"check_in": check_in, "mode": mode, "message": message, "recommended_strategy": recommended_strategy,})

    else:
        form = DailyCheckInForm()
        
    return render(request, "wellbeing/daily_reset.html", {"form": form,})
        
    

    
    