import random
from .models import Strategy

MODE_CATEGORY_MAP = {
    "Recovery Mode": "recovery",
    "Low-Energy Mode": "starting",
    "Steady Mode": "organisation",
    "Balanced Mode": "focus",
    "Progress Mode": "study",
}

def daily_tip(request):
    if not request.user.is_authenticated:
        return {}

    last_reset_mode = request.COOKIES.get("last_reset_mode")
    category = MODE_CATEGORY_MAP.get(last_reset_mode)

    strategies = Strategy.objects.filter(active=True)
    if category:
        matching = strategies.filter(category=category)
        if matching.exists():
            strategies = matching

    strategies = list(strategies)
    tip = random.choice(strategies) if strategies else None

    return {"daily_tip": tip}