import base64
import time

import requests
from django.conf import settings
from django.shortcuts import render
from datetime import date as date_cls, datetime, timedelta

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def weather_api(request):
    city ="Karczowiska"
    lat = 51.24
    lon = 16.12
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()

        if resp.status_code == 200:
            weather_data ={
                'city': city,
                'temp': data['main']['temp'],
                'description':data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
            return Response(weather_data, status = status.HTTP_200_OK)
        else:
            return Response(
                {'error': data.get('message', 'Błąd pobierania pogody.')},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': 'Błąd połączenia.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def weather(request):
    city = "Karczewiska"
    lat = 51.24
    lon = 16.12
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    weather = {}
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            weather = {
                'city': city,
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
        else:
            weather['error'] = data.get('message', 'Błąd pobierania pogody.')
    except Exception:
        weather['error'] = 'Błąd połączenia.'

    return render(request, "apis_app/apis_template.html", {'weather': weather})

def holiday(request):
    today= datetime.now().date()
    year = today.year
    month = today.month
    day = 1
    holidays= []
    api_key = settings.HOLIDAYS_API_KEY

    for i in range(1,12):
        url = f"https://holidays.abstractapi.com/v1/?api_key={api_key}&country=PL&year={year}&month={month}&day={i}"
        resp = requests.get(url, timeout=5)
        holiday = resp.json()
        if holiday:
            holidays.append(holiday)

        time.sleep(1)

    print(holidays)
    return render(request, "apis_app/apis_template.html", {
        'holidays': holidays})

def exchange(request):
    context ={}

    if request.method == "POST":
        url2 = f"https://avatars.abstractapi.com/v1/?api_key=7f54735162a745ae97ce10d1356e4d4b&name=Claire Florentz"
        response2 = requests.get(url2, timeout=5)
        avatar_base64 = base64.b64encode(response2.content).decode('utf-8')
        context['avatar'] = avatar_base64
        currency_from = request.POST.get('currency_from', '').upper()
        currency_to = request.POST.get('currency_to', '').upper()

        if currency_from and currency_to:
            api_key = settings.EXCHANGE_API_KEY
            url = f"https://exchange-rates.abstractapi.com/v1/live/?api_key={api_key}&base={currency_from}&target={currency_to}"
            try:
                response = requests.get(url, timeout=5)
                exchange_info = response.json()
                context['exchange_info'] = exchange_info

                if response.status_code == 200:
                    from_currency = exchange_info['base']
                    currency_rate = exchange_info['exchange_rates'].get(currency_to)

                    if currency_rate:
                        context['from_currency'] = from_currency
                        context['to_currency'] = currency_to
                        context['currency_rate'] = currency_rate
                    else:
                        context['error'] = f'Brak kursu dla {currency_to}'
                else:
                    context['error'] = 'Błąd API'
            except Exception as e:
                context['error'] = f'Błąd połączenia: {str(e)}'
        else:
            context['error'] = 'Wypełnij oba pola !'
    return render(request, "apis_app/apis_template.html", context)



import google.generativeai as genai

def workout_generator(request):
    context = {}

    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        ai_workout_description = request.POST.get('workout_detail_type')

        if prompt:
            if ai_workout_description == 'detailed':
                try:
                    genai.configure(api_key=settings.GEMINI_API_KEY)
                    model = genai.GenerativeModel('gemini-2.5-pro')

                    response = model.generate_content(
                        f"""Wygeneruj plan treningu dla: {prompt}
                        
                        Zwróć TYLKO czysty JSON w formacie:
                        {{
                          "exercises": [
                            {{
                              "name": "Wyciskanie sztangi",
                              "sets": [
                                {{"weight": 60, "reps": 10}},
                                {{"weight": 70, "reps": 8}}
                              ]
                            }}
                          ]
                        }}
                        
                        Bez żadnych dodatkowych tekstów, TYLKO JSON."""
                    )

                    ai_workout_json = response.text.strip()
                    # Usuń markdown jeśli AI dodało ```json
                    if ai_workout_json.startswith('```'):
                        ai_workout_json = ai_workout_json.split('```')[1]
                        if ai_workout_json.startswith('json'):
                            ai_workout_json = ai_workout_json[4:]

                    ai_workout_json = ai_workout_json.strip()

                    context['ai_workout_json'] = ai_workout_json
                    context['prompt'] = prompt

                except Exception as e:
                    context['error'] = f'Błąd: {str(e)}'


            elif ai_workout_description == 'description':
                try:
                    genai.configure(api_key=settings.GEMINI_API_KEY)
                    model = genai.GenerativeModel('gemini-2.5-pro')

                    response = model.generate_content(
                        f"""
                        Jesteś trenerem fitness piszącym plany treningowe.
                        
                        Napisz szczegółowy plan treningu: {prompt}
                        
                        Format:
                        - Rozgrzewka (2-3 zdania)
                        - Główna część (lista ćwiczeń z opisem)
                        - Rozciąganie (2-3 zdania)
                        
                        Styl: 
                            *jak najmniej zbednej treści,
                            *ogranicz sie do wypisania cwiczen i zakresów
                            *każde zdanie z nowej linii, 
                            *motywujący, konkretny.
                            *bez wstępu typu "hej biegaczu"
                        
                        Długość: max. 100 słów.
                        """
                    )

                    ai_workout_text = response.text.strip()
                    # Usuń markdown jeśli AI dodało ```
                    if ai_workout_text.startswith('```'):
                        ai_workout_text = ai_workout_text.split('```')[1]


                    context['ai_workout_text'] = ai_workout_text
                    context['prompt'] = prompt

                except Exception as e:
                    context['error'] = f'Błąd: {str(e)}'
        else:
            context['error'] = 'Wpisz czego szukasz'

    return render(request, 'apis_app/workout_generator.html', context)














































