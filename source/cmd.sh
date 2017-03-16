#!/usr/bin/env bash
# This script is run from within the running container.
set -e


echo "Starting service in $NC_CONFIGURATION mode"

if [[ "$NC_CONFIGURATION" == @("development"|"test") ]]; then
    exec python server_flask.py
else
    # Acceptance, production
    exec uwsgi uwsgi.ini
fi
