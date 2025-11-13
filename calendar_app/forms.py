from django import forms
from .models import Reminder, DayNote


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["date", "time", "title", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "title": forms.TextInput(attrs={"placeholder": "Tytuł przypomnienia"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Opis (opcjonalnie)"}),
        }


class DayNoteForm(forms.ModelForm):
    class Meta:
        model = DayNote
        fields = ["date", "text"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "text": forms.Textarea(attrs={"rows": 4, "placeholder": "Co zrobiłeś/aś tego dnia?"}),
        }
