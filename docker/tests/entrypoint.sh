#!/bin/sh

set -o errexit
set -o nounset

timeout 60s bash -c "until pg_isready -d $DATABASE_URL; do sleep 5; done"

exec "$@"
