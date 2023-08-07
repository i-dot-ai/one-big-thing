#!/bin/sh

set -o errexit
set -o nounset

DATABASE_URL_VARIABLE_NAME="${ENVIRONMENT}_DATABASE_URL"
DATABASE_URL_VALUE=$(eval "echo \$$DATABASE_URL_VARIABLE_NAME")

echo $DATABASE_URL_VALUE

wait-for-db --mode postgres --connection-string $DATABASE_URL_VALUE --timeout 60 --sql-query "select 1;"

exec "$@"
