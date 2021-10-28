#!/bin/sh

set -e

python manage.py collectstatic --noinput

uwsgi --module eCommerce.wsgi --socket :8000 --master --enable-threads