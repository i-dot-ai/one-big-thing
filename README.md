This purpose of this project is to create a "One Big Thing Learning Record" for the tracking of civil servants learning. This will allow users and auditors across government to review what training civil servants are completing and get survey data on their progress.

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

1. in docker, as used in CI
```commandline
make test
```

2. locally, e.g. so you can debug in an IDE
```commandline
POSTGRES_HOST=localhost python -m pytest
```
note that this assumes that postgres is running in docker, if in doubt run `docker-compose up -d db` first

## To update the allowed email domains

Update the list in `one_big_thing/learning/domains.py`. We currently allow all `gov.uk` domains, and all domains in that list (including subdomains).

Note that once changes to the domains have been made, they will need to be deployed to take effect.

## Running management commands in dev and prod
A limited number of management commands can be run on the `dev` and `prod` environment. If you want to run your command remotely, it will need to be added to the `manage_remote.py` file.

Obviously great care needs to be taken when running against `prod`! 

In order to run the commands you will need:
1. to have (AWS credentials)[https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html] set up 
2. to have the relevant packages, boto3 and click, installed before running

Commands can then be run like:

`python -m manage_remote user-stats --env dev`

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
  get-learning-breakdown-data Replicate the data from the API
  get-signups-by-date Replicate the data from the API
 ```

If your command prints things to the console (most of them do), you will have to run `get-logs` after you've run the command to see the logs.

## How to access the admin

Access to the admin is authenticated via username & password and TOTP and authorized for `staff` users.

If you are the first person to get access in any given environment, e.g. your own local env or
a new AWS test env then

1. make yourself a superuser `docker compose run web python manage.py assign_superuser_status --email your-email-address@cabinetoffice.gov.uk --pwd y0urP4ssw0rd`, you dont need to set the password if you already have one.
2. copy the link generated by the step above and open it on your phone to create a new TOTP account
3. log in to the admin localhost/admin with your email, password and TOTP code generated on your phone/other device.

Otherwise speak to an existing admin to edit your account.
