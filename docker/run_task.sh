#!/usr/bin/env bash

set -x
set -e

docker-compose run --rm app bash -l -c "python -m $@"
