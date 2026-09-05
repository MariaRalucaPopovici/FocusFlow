from django import forms
from .models import DailyCheckIn


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
        
        
            