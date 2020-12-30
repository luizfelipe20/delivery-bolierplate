#!/bin/sh

pip install --upgrade pip
pip install --upgrade Pillow
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn delivery.wsgi --bind=0.0.0.0:80

