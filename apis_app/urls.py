from django.urls import path
from . import views
from calendar_app.views import DayView, AddNoteView, AddReminderView, ToggleReminderView, DeleteReminderView, DeleteNoteView

app_name = "apis_app"

urlpatterns = [
    path('weather/', views.weather, name='weather'),
    path('weather_api/', views.weather_api, name='weather_api'),
    path('holiday/', views.holiday, name='holiday'),
    path('exchange/', views.exchange, name='exchange'),
    path('workout_generator/', views.workout_generator, name='workout_generator'),
]