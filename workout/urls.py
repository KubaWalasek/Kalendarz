from django.urls import path
from .views import AddWorkoutView, SaveDescriptionView, SaveDetailedView, WorkoutDisplayView, WorkoutListView

app_name = 'workout'



urlpatterns = [
    path('add_workout/', AddWorkoutView.as_view(), name='add_workout'),
    path('save_workout_description/', SaveDescriptionView.as_view(), name='save_workout_description'),
    path('save_workout_detailed/', SaveDetailedView.as_view(), name='save_workout_detailed'),
    path('workout_display/<int:pk>', WorkoutDisplayView.as_view(), name='workout_display'),
    path('workout_list/', WorkoutListView.as_view(), name='workout_list')
]