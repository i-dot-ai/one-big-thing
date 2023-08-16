#!/bin/sh

set -o errexit
set -o nounset

if [ "$DEBUG" = true ]
then
  wait-for-db --mode postgres --connection-string "$DATABASE_URL" --timeout 60 --sql-query "select 1;"
fi

exec "$@"
