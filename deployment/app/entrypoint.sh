#!/bin/sh

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

uvicorn --host 0.0.0.0 --port 8001 redirectplatform.asgi:application --reload --reload-include *.html