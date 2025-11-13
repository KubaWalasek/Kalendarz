from django.db import models

from CalendarApp import settings

WORKOUT_NAME_CHOICES= [
    ('Weightlifting', 'Weightlifting'),
    ('Cardio', 'Cardio'),
    ('Crossfit', 'Crossfit'),
    ('Kettlebell', 'Kettlebell'),
    ('Yoga', 'Yoga'),
    ('Boxing', 'Boxing'),
    ('Running', 'Running'),
    ('Swimming', 'Swimming'),
    ('Tennis', 'Tennis'),
    ('Gymnastics', 'Gymnastics'),
    ('Horse Riding', 'Horse Riding'),
    ('Other', 'Other')
]

class Workout(models.Model):
    date = models.DateField()
    type = models.CharField(choices=WORKOUT_NAME_CHOICES, default='Weightlifting')
    name = models.CharField(max_length=100, blank=True, help_text='Nazwij swój trening, np. KLATA, NOGI...')
    set = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} | {self.name}' if self.name else f'{self.date} | {self.type}'




