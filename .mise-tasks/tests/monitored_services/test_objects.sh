#!/bin/bash
#MISE alias="test_objects"
#MISE description="Test Nobbomb monitored service objects"

source .mise-tasks/variables/main.sh
source .mise-tasks/variables/computed.sh

export PYTEST_ADDOPTS="--color=yes"
export DEBUG_MODE=true
export PYTHONPATH=src

pytest src/tests/test_objects.py -v -s --log-cli-level=DEBUG 2>&1 | tee test_objects.json