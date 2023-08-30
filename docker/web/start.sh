#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate --noinput

echo "Migrations completed"

python manage.py add_special_courses

echo "Added special courses"

echo "Starting app"

echo "Using '$ENVIRONMENT' environment settings"

if [ "$ENVIRONMENT" = "LOCAL" ]
then
    gunicorn --reload --workers 3 one_big_thing.wsgi:application
else
    gunicorn --workers 3 one_big_thing.wsgi:application
fi
