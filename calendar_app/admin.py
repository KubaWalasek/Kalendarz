
from django.contrib import admin
from .models import Reminder, DayNote, CalendarBackground

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


@admin.register(CalendarBackground)
class CalendarBackgroundAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'image']
    list_filter = ['is_active', 'created_at']
    actions = ['activate_background']

    def activate_background(self, request, queryset):
        # Wyłącz wszystkie
        CalendarBackground.objects.update(is_active=False)
        # Włącz wybrane (tylko pierwsze jeśli zaznaczono wiele)
        first = queryset.first()
        if first:
            first.is_active = True
            first.save()
        self.message_user(request, f"Tło '{first.name}' zostało aktywowane")
    activate_background.short_description = "Aktywuj wybrane tło"