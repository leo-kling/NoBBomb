#!/bin/bash
#MISE alias="test_kill_switch"
#MISE description="Test NoBBomb kill switch"

source .mise-tasks/variables/main.sh
source .mise-tasks/variables/computed.sh

export PYTEST_ADDOPTS="--color=yes"
export DEBUG_MODE=true
export PYTHONPATH=src

pytest src/tests/test_kill_switch.py -v -s --log-cli-level=DEBUG 2>&1 | tee test_kill_switch.json