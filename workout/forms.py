from django import forms
from .models import Workout, WORKOUT_NAME_CHOICES

class WorkoutForm(forms.ModelForm):
    workout_detail_type = forms.ChoiceField(
        choices=[
            ('description', 'Tylko opis'),
            ('detailed', 'Plan')],
        widget = forms.RadioSelect,
        initial='description',
        label='Plan treningu'
    )
    class Meta:
        model = Workout
        fields = ['name', 'date', 'type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'type': forms.Select(choices=WORKOUT_NAME_CHOICES)
        }

class WorkoutDescriptionForm(forms.Form):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Opis treningu'
    )