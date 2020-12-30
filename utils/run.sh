#!/bin/sh

python -m pip install --upgrade pip
python -m pip install --upgrade Pillow
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn django_project.wsgi --bind=0.0.0.0:80

