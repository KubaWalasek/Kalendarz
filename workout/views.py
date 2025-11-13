from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import WorkoutForm, WorkoutDescriptionForm
from .models import Workout
import json

class AddWorkoutView(LoginRequiredMixin, View):
    def get(self, request):
        form = WorkoutForm()
        return render(request, 'add_workout.html', {'form': form})

    def post(self, request):
        form = WorkoutForm(request.POST)
        user = request.user
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = user
            workout_detail_type = form.cleaned_data['workout_detail_type']

            if workout_detail_type == 'description':
                return render(request, 'workout_description.html', {
                    'workout': workout,
                    'description_form': WorkoutDescriptionForm()
                })
            else:
                return render(request, 'workout_detailed.html', {
                    'workout': workout,
                })
        else:
            form = WorkoutForm()

        return render(request, 'add_workout.html', {'form': form})


class SaveDescriptionView(LoginRequiredMixin, View):
    def post(self, request):
        form = WorkoutDescriptionForm(request.POST)
        if form.is_valid():
            # Tworzenie obiektu Workout
            workout = Workout.objects.create(
                user=request.user,
                date=request.POST.get('workout_date'),
                type=request.POST['type'],
                name=request.POST.get('name'),
                set={
                    'type': 'description',
                    'text': form.cleaned_data['description']
                }
            )
            # Przekierowanie po zapisaniu (możesz zmienić na swój URL)
            return redirect('calendar_app:month')

        # Jeśli formularz nieprawidłowy, wróć z błędami
        return render(request, 'workout_description.html', {
            'description_form': form,
            'workout': {
                'date': request.POST.get('date'),
                'type': request.POST.get('type')
            }
        })

class SaveDetailedView(LoginRequiredMixin, View):
    def post(self, request):

        # Podstawowe dane treningu
        workout_date = request.POST.get('workout_date')
        workout_type = request.POST.get('type')
        workout_name = request.POST.get('name')

        # Zbierz wszystkie ćwiczenia z POST danych
        exercises_dict = {}

        for key, value in request.POST.items():
            if key.startswith('exercise_') and '_name' in key:
                # exercise_1_name -> exercise_num = 1
                exercise_num = key.split('_')[1]
                exercises_dict[exercise_num] = {
                    'name': value,
                    'sets': []
                }

        # Zbierz serie dla każdego ćwiczenia
        for key, value in request.POST.items():
            if 'set_' in key and ('weight' in key or 'reps' in key or 'done' in key):
                # exercise_1_set_2_weight -> [exercise_1, set_2, weight]
                parts = key.split('_')
                if len(parts) >= 4:
                    exercise_num = parts[1]
                    set_num = parts[3]
                    field_type = parts[4]  # weight lub reps lub done

                    if exercise_num in exercises_dict:
                        # Znajdź lub utwórz serię
                        sets = exercises_dict[exercise_num]['sets']
                        set_obj = None

                        # Znajdź istniejącą serię o tym numerze
                        for s in sets:
                            if s.get('set_number') == set_num:
                                set_obj = s
                                break

                        # Jeśli nie ma, utwórz nową
                        if not set_obj:
                            set_obj = {'set_number': set_num, 'weight': 0.0, 'reps': 0, 'done': 0}
                            sets.append(set_obj)

                        # Ustaw wartość
                        if field_type == 'weight':
                            set_obj['weight'] = float(value) if value and value.strip() else 0.0
                        elif field_type == 'reps':
                            set_obj['reps'] = int(value) if value and value.strip() else 0
                        elif field_type == 'done':
                            set_obj['done'] = int(value) if value and value.strip() else 0

        # Konwertuj na listę
        exercises = []
        for exercise_data in exercises_dict.values():
            if exercise_data['sets']:  # Tylko jeśli ma serie
                # Usuń set_number z każdej serii (nie potrzebujemy go w JSON)
                clean_sets = []
                for set_data in exercise_data['sets']:
                    clean_sets.append({
                        'weight': set_data['weight'],
                        'reps': set_data['reps'],
                        'done': set_data['done']
                    })

                exercises.append({
                    'name': exercise_data['name'],
                    'sets': clean_sets
                })

        print(f"Parsed exercises: {exercises}")

        # Zapisanie do bazy
        workout = Workout.objects.create(
            user=request.user,
            date=workout_date,
            type=workout_type,
            name=workout_name,
            set={
                'type': 'detailed',
                'exercises': exercises
            }
        )

        return redirect('calendar_app:month')


class WorkoutListView(LoginRequiredMixin, View):
    def get(self, request):
        workouts = Workout.objects.filter(user=request.user).order_by('-date')
        return render(request, 'workout_list.html', {'workouts': workouts})


class WorkoutDisplayView(LoginRequiredMixin, View):
    def get(self, request,pk):
        workout = Workout.objects.get(pk=pk, user=request.user)
        return render(request, 'workout_display.html', {'workout': workout})