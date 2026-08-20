from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    deadline = forms.SplitDateTimeField(
        required=False,
        widget=forms.SplitDateTimeWidget(
            date_attrs={
                "type": "date",
                "class": "date-input"
            },
            time_attrs={
                "type": "time",
                "class": "time-input"
            },
        )
    )

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "deadline",
            "urgent",
            "important",
        ]