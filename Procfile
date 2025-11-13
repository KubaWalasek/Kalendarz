web: gunicorn CalendarApp.wsgi --bind 0.0.0.0:$PORT --log-file -
release: python manage.py collectstatic --noinput && python manage.py migrate