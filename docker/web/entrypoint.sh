#!/bin/sh

set -o errexit

if [ "$DEBUG" = true ] && [ -z "$DATABASE_URL" ]
then
  wait-for-db --mode postgres --connection-string "$DATABASE_URL" --timeout 60 --sql-query "select 1;"
fi

exec "$@"
