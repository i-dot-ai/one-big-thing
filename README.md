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

## To update the allowed domains

Currently we use a list provided to us for the list of allowed domains. To access this, a direct link to the gist is needed.
Contact Sam, Ell or Nina for a link to the document. The url to the `raw` version of the CSV is needed, not the link to the parsed gist.

To get the list of domains, run this command on the container:

    python manage.py get_domains

The list of domains are needed in an env var, currently stored in a github secret. To get the values in the right format for a github secret:

- copy the created list from the console of the above command.
- create a scratch file
- Copy the list into the scratch file
- Add the following code to the scratch file

        domains = ', '.join(CIVIL_SERVICE_DOMAINS)
        print(domains)

- run the scratch file
- Copy the resulting string into a github secret called `ALLOWED_DOMAINS`

### Adding a new domain that's not in the given list

If there is a domain that isn't in the given list, run the above scenario, then in the resulting string add your desired domain before saving the github secret.

Example

        ["example.com", "test.com", "desired-domain.com"]