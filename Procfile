web: python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn congif.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --log-file -
