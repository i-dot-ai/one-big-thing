#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate --noinput

echo "Migrations completed"

python manage.py add_special_courses

echo "Added special courses"

echo "Starting app"

echo "Using '$ENVIRONMENT' environment settings"

PORT_VARIABLE_NAME="${ENVIRONMENT}_PORT"
PORT_VALUE=$(eval "echo \$$PORT_VARIABLE_NAME")

watchmedo auto-restart --directory=./  --pattern=""*.py"" --recursive -- waitress-serve --port=$PORT_VALUE --threads=8 one_big_thing.wsgi:application
