#!/usr/bin/env bash
set -e


docker build -t test/nc_plan .
docker run \
    --env NC_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/nc_plan:/nc_plan \
    test/nc_plan
