#!/usr/bin/env bash

set -e
set -x

bash ./scripts/lint.sh
pytest --cov=driganttic --cov=tests --cov-report=html tests "${@}"
