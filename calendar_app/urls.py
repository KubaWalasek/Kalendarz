from django.urls import path
from . import views
from .views import DayView, AddNoteView, AddReminderView, ToggleReminderView, DeleteReminderView, DeleteNoteView

app_name = "calendar_app"

urlpatterns = [
    path("", views.month_view, name="month"),
    path("<int:year>/<int:month>/", views.month_view, name="month"),
    path("day/<int:year>/<int:month>/<int:day>/", DayView.as_view(), name="day"),
    path("reminder/add/", AddReminderView.as_view(), name="add_reminder"),
    path("note/add/", AddNoteView.as_view(), name="add_note"),
    path("reminder/<int:pk>/toggle/", ToggleReminderView.as_view(), name="toggle_reminder"),
    path("reminder/<int:pk>/delete/", DeleteReminderView.as_view(), name="delete_reminder"),
    path("note/<int:pk>/delete/", DeleteNoteView.as_view(), name="delete_note"),
]
