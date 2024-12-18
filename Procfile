web: gunicorn dashboard.wsgi --log-file -
web: python manage.py migrate && gunicorn dashboard.wsgi