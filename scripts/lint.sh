#!/usr/bin/env bash

set -e
set -x

poetry run black driganttic tests --check
poetry run ruff driganttic tests
poetry run mypy driganttic
