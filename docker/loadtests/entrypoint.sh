#!/bin/sh

set -o errexit
set -o nounset

exec locust -f ./locustfile.py "$@"
