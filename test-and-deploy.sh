#!/usr/bin/env bash

set -euo pipefail

pipenv install
( cd src/object_lambda; pip install --upgrade -t vendored -r requirements.txt )
pipenv run pytest
pipenv run cdktf deploy
