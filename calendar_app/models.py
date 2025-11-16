from django.db import models

from CalendarApp import settings


class DayNote(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["date"]),
        ]
        verbose_name = "Notatka dnia"
        verbose_name_plural = "Notatki dnia"

    def __str__(self):
        return f"Notatka {self.date}: {self.text[:20]}" if self.text else f"Notatka {self.date}"


class Reminder(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(db_index=True)
    time = models.TimeField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["completed", "time", "title"]
        indexes = [
            models.Index(fields=["date"]),
        ]
        verbose_name = "Przypomnienie"
        verbose_name_plural = "Przypomnienia"

    def __str__(self):
        t = f" {self.time}" if self.time else ""
        done = "✓ " if self.completed else ""
        return f"{done}{self.date}{t} — {self.title}"


class CalendarBackground(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa tła")
    image = models.ImageField(upload_to='backgrounds/', verbose_name="Zdjęcie")
    is_active = models.BooleanField(default=False, verbose_name="Aktywne")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tło kalendarza"
        verbose_name_plural = "Tła kalendarza"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_active:
            CalendarBackground.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
