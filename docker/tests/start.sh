#!/bin/sh

set -o errexit
set -o nounset

python manage.py migrate --noinput

python manage.py add_special_courses

echo "Added special courses"

echo
echo '----------------------------------------------------------------------'
echo
nosetests -v ./tests --logging-level=ERROR --with-coverage --cover-package=one_big_thing
