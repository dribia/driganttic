#!/usr/bin/env bash

set -e
set -x

mypy driganttic
flake8 driganttic tests
black driganttic tests --check
isort driganttic tests --check-only
pydocstyle driganttic
