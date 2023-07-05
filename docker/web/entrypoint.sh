#!/bin/sh

set -o errexit
set -o nounset

wait-for-db --mode postgres --connection-string $DATABASE_URL --timeout 60 --sql-query "select 1;"

exec "$@"
