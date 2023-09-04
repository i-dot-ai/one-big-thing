This purpose of this project is to create a "One Big Thing Learning Record" for the tracking of Civil Servants learning. This will allow users and auditors across government to review what training Civil Servants are completing and get survey data on their progress.

## How to run

To run this project:

    docker-compose up --build --force-recreate web

open http://localhost:8055/

To populate the database with fake data:

    docker-compose run web python manage.py add_courses

To reset the database:

    make reset-db

To check for syntax errors:

    make check-python-code

To update the requirement lockfiles:

    make update-requirements

To run tests:

    make test

## To update the allowed email domains

Update the list in `one_big_thing/learning/domains.py`. We currently allow all `gov.uk` domains, and all domains in that list (including subdomains).

Note that once changes to the domains have been made, they will need to be deployed to take effect.