from datetime import date as date_cls, datetime, timedelta
import calendar

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST

from workout.models import Workout
from .models import DayNote, Reminder
from .forms import ReminderForm, DayNoteForm


def month_view(request: HttpRequest, year: int | None = None, month: int | None = None) -> HttpResponse:
    user = request.user
    today = datetime.now().date() #dzisiejsza data
    if year is None or month is None:
        year, month = today.year, today.month #dzisiaj mesiac , dzisiaj rok
    first_day = date_cls(year, month, 1)   #tworzmy date pierwszego dnia
    _, days_in_month = calendar.monthrange(year, month) #ile dni ma dany miesiac

    # Determine the first day to show (start from Monday)
    start_weekday = (first_day.weekday())  # Monday=0 określa jaki to dzień tygodnia
    grid_start = first_day - timedelta(days=start_weekday)  # okresla date dnia na pierwszy kafelek w linii kalendarza
    # 6 weeks grid (42 days)
    days = [grid_start + timedelta(days=i) for i in range(42)] #lista dni siatki kalendarza w danym miesiącu

    prev_month_date = (first_day - timedelta(days=1)).replace(day=1)
    next_month_year = year + (1 if month == 12 else 0)
    next_month_month = 1 if month == 12 else month + 1
    next_month_date = date_cls(next_month_year, next_month_month, 1)

    # Prefetch reminders/notes for all days in grid
    dates_set = {d for d in days}

    if user.is_authenticated:
        reminders = Reminder.objects.filter(author=user, date__in=dates_set).order_by("time")
        notes = DayNote.objects.filter(author=user, date__in=dates_set)
        workouts = Workout.objects.filter(user=user, date__in=dates_set)

        reminders_map: dict[date_cls, list[Reminder]] = {d: [] for d in days}
        for r in reminders:
            reminders_map.setdefault(r.date, []).append(r)

        notes_map: dict[date_cls, list[DayNote]] = {d: [] for d in days}
        for n in notes:
            notes_map.setdefault(n.date, []).append(n)

        workouts_map: dict[date_cls, list[Workout]] = {d: [] for d in days}
        for w in workouts:
            workouts_map.setdefault(w.date, []).append(w)

        day_items = [{
            "date": d,
            "reminders": reminders_map.get(d, []),
            "notes": notes_map.get(d, []),
            "workouts": workouts_map.get(d, []),
            "is_other": d.month != month,
        } for d in days]
    else:
        day_items = [{
            "date": d,
            "is_other": d.month != month,
        } for d in days]

    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month].capitalize(),
        "days": day_items,
        "today": today,
        "current_month": first_day,
        "prev_month": {"year": prev_month_date.year, "month": prev_month_date.month},
        "next_month": {"year": next_month_date.year, "month": next_month_date.month},
        'url': 'month',
        'background_image': request.session.get('background_image'),
    }

    return render(request, "calendar_app/month.html", context )


class DayView(LoginRequiredMixin, View):
    def get(self, request, year, month, day):
        the_date = date_cls(year, month, day)
        days_pl = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
        day_name  = days_pl[the_date.weekday()]
        user = request.user
        reminders = Reminder.objects.filter(author=user, date=the_date).order_by("completed", "time")
        notes = DayNote.objects.filter(author=user, date=the_date).order_by("-created_at")
        workouts = Workout.objects.filter(user=user, date=the_date).order_by("-date")
        reminder_form = ReminderForm(initial={"date": the_date.isoformat()}) #rózne sposoby formatowania daty
        note_form = DayNoteForm(initial={"date": the_date.strftime('%Y-%m-%d')}) #zeby html ogarnal i z automatu wypelnil form

        # For base header navigation
        first_day = date_cls(the_date.year, the_date.month, 1)
        next_day = the_date + timedelta(days=1)
        prev_day = the_date - timedelta(days=1)
        prev_month_date = (first_day - timedelta(days=1)).replace(day=1)
        next_month_year = the_date.year + (1 if the_date.month == 12 else 0)
        next_month_month = 1 if the_date.month == 12 else the_date.month + 1
        next_month_date = date_cls(next_month_year, next_month_month, 1)

        return render(request, "calendar_app/day.html", {
            "date": the_date,
            "reminders": reminders,
            "notes": notes,
            "workouts": workouts,
            "reminder_form": reminder_form,
            "note_form": note_form,
            "today": datetime.now().date(),
            "prev_month": {"year": prev_month_date.year, "month": prev_month_date.month},
            "next_month": {"year": next_month_date.year, "month": next_month_date.month},
            "day_name": day_name,
            'next_day': next_day,
            'prev_day': prev_day,
            'url': 'day'
        })



class AddReminderView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.author = user
            reminder.save()
            return redirect("calendar_app:day", year=reminder.date.year, month=reminder.date.month, day=reminder.date.day)
        # If invalid, fall back to month of provided date or today
        d = form.data.get("date")
        try:
            y, m, dd = map(int, d.split("-"))
            return redirect("calendar_app:day", year=y, month=m, day=dd)
        except Exception:
            today = datetime.now().date()
            return redirect("calendar_app:month", year=today.year, month=today.month)



class AddNoteView(LoginRequiredMixin, View):
    def post(self, request):
        form = DayNoteForm(request.POST)
        user = request.user
        if form.is_valid():
            note = form.save(commit=False)
            note.author = user
            note.save()
            return redirect("calendar_app:day", year=note.date.year, month=note.date.month, day=note.date.day)
        d = form.data.get("date")
        try:
            y, m, dd = map(int, d.split("-"))
            return redirect("calendar_app:day", year=y, month=m, day=dd)
        except Exception:
            today = datetime.now().date()
            return redirect("calendar_app:month", year=today.year, month=today.month)



class ToggleReminderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reminder = get_object_or_404(Reminder, pk=pk)
        reminder.completed = not reminder.completed
        reminder.save(update_fields=["completed"])
        return redirect("calendar_app:day", year=reminder.date.year, month=reminder.date.month, day=reminder.date.day)



class DeleteReminderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reminder = get_object_or_404(Reminder, pk=pk)
        y, m, d = reminder.date.year, reminder.date.month, reminder.date.day
        reminder.delete()
        return redirect("calendar_app:day", year=y, month=m, day=d)



class DeleteNoteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        note = get_object_or_404(DayNote, pk=pk)
        y, m, d = note.date.year, note.date.month, note.date.day
        note.delete()
        return redirect("calendar_app:day", year=y, month=m, day=d)


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        przeslany_plik_obraz = request.FILES['image']
        system_plikow = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
        zapisana_nazwa_pliku = system_plikow.save(przeslany_plik_obraz.name, przeslany_plik_obraz)
        adres_url_zapisanego_pliku = system_plikow.url(zapisana_nazwa_pliku)

        request.session['background_image'] = adres_url_zapisanego_pliku

        return redirect('calendar_app:month')

    return render(request, 'calendar_app/upload_image.html')