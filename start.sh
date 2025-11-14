#!/bin/bash

echo "=== Starting deployment ==="
echo "DATABASE_URL is set: $DATABASE_URL"

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Starting gunicorn ==="
exec gunicorn CalendarApp.wsgi:application --bind 0.0.0.0:$PORT --log-file -