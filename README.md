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

## running management commands in dev and prod
A limited number of management commands can be run on the `dev` and `prod` environment.

Obviously great care needs to be taken when running against `prod`! 

In order to run the commands you will need:
1. to have (AWS credentials)[https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html] set up 
2. to have the relevant packages, boto and click, installed before running

Commands can then be run like:

`python -m remote_manage --env dev user-stats`

Documentation for each command can be access with `--help`

```commandline
$ python -m manage_remote --help
Usage: manage_remote.py [OPTIONS] COMMAND [ARGS]...

  execute a limited number of management commands remotely

Options:
  --help  Show this message and exit.

Commands:
  get-logs
  user-stats  gather user stats.
 ```
