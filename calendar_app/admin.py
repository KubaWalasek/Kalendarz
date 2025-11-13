from django.contrib import admin
from .models import Reminder, DayNote


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "title", "completed")
    list_filter = ("date", "completed")
    search_fields = ("title", "description")
    ordering = ("-date", "time")


@admin.register(DayNote)
class DayNoteAdmin(admin.ModelAdmin):
    list_display = ("date", "short_text", "created_at")
    list_filter = ("date",)
    search_fields = ("text",)
    ordering = ("-date", "-created_at")

    def short_text(self, obj):
        return (obj.text[:60] + "…") if len(obj.text) > 60 else obj.text
    short_text.short_description = "Tekst"
