from django import forms
from .models import DailyCheckIn, Routine


class DailyCheckInForm(forms.ModelForm):
    energy = forms.ChoiceField(
        choices=DailyCheckIn.ENERGY_CHOICES,
        widget=forms.RadioSelect
    )
    mood = forms.ChoiceField(
        choices=DailyCheckIn.MOOD_CHOICES,
        widget=forms.RadioSelect
    )
    class Meta:
        model = DailyCheckIn
        fields = [
            "energy",
            "mood",
            "note",
        ]
        
        labels = {
            "energy": "How much capacity do you have today?",
            "mood": "How are you feeling?",
            "note": "Anything you want to get out of your head?",
        }

        widgets = {
            "note": forms.Textarea(attrs={"placeholder": "Optional - thoughts, worries, reminders...","rows": 4,}),
        }
        


class RoutineForm(forms.ModelForm):
    steps_text = forms.CharField(
        label="Steps (one per line, in the order you'll do them)",
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Drink a glass of water\nCheck today's top 3 tasks\n5-minute stretch"}),
        required=False,
    )

    class Meta:
        model = Routine
        fields = ["title", "description", "mode", "routine_type"]