release: python manage.py migrate --noinput
web: gunicorn ecommerce.wsgi --bind 0.0.0.0:$PORT
