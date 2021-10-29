#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations

uwsgi --module eCommerce.wsgi --socket :8000 --master --enable-threads