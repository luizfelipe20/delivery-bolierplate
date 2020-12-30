#!/bin/sh

python -m pip install --upgrade pip
python -m pip install --upgrade Pillow
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn delivery.wsgi --bind=0.0.0.0:80

