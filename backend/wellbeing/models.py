from django.db import models
from django.contrib.auth.models import User

class DailyCheckIn(models.Model):
    ENERGY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("good", "Good"),
    ]
    MOOD_CHOICES = [
        ("calm", "Calm"),
        ("okay", "Okay"),
        ("stressed", "Stressed"),
        ("overwhelmed", "Overwhelmed"),
        ("motivated", "Motivated"),
        ("tired", "Tired"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    energy = models.CharField(max_length=10, choices=ENERGY_CHOICES)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    note = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.energy}"
    
class Strategy(models.Model):
    CATEGORY_CHOICES = [
        ("focus", "Focus"),
        ("starting", "Getting Started"),
        ("organisation", "Organisation"),
        ("recovery", "Recovery"),
        ("study", "Study"),
        ("routine", "Routine"),
    ]
    
    ENERGY_CHOICES = [
        ("any", "Any"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("good", "Good"),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    short_tip = models.CharField(
        max_length=150,
        blank=True,
        help_text="A short, one-line version of this strategy, used for the pop-up tip. Leave blank to fall back to a trimmed description.",
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    energy_level = models.CharField(max_length=20, choices=ENERGY_CHOICES, default="any")
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    resource_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Strategies"
    
class Routine(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="routines")
    
    MODE_CHOICES = [
        ("recovery", "Recovery"),
        ("low_energy", "Low Energy"),
        ("steady", "Steady"),
        ("balanced", "Balanced"),
        ("progress", "Progress"),
    ]
    
    ROUTINE_TYPE_CHOICES = [
        ("morning", "Morning"),
        ("study", "Study"),
        ("cleaning", "Cleaning"),
        ("cooking", "Cooking"),
        ("evening", "Evening"),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    routine_type = models.CharField(max_length=20, choices=ROUTINE_TYPE_CHOICES)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class RoutineStep(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE,related_name="steps")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveIntegerField(default=1)
    strategy = models.ForeignKey(Strategy, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.routine.title} - {self.title}"
    
    class Meta:
        ordering = ["order"]

class DopamineMenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("starters", "Starters (10-15 minutes)"),
        ("mains", "Mains (about an hour)"),
        ("sides", "Sides (alongside something else)"),
        ("desserts", "Desserts (good in moderation)"),
        ("specials", "Specials (rare treats)"),
        ("salads", "Salads (good for you, harder to start)"),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_entries")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ["-created_at"]