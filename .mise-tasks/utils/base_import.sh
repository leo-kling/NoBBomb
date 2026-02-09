#!/bin/bash
#MISE alias="base_import"
#MISE description="Base import Variables/Constants and Helpers for bash/mise tasks"

# Variables / Constants
source ./config.sh
source .mise-tasks/variables/main.sh
source .mise-tasks/variables/computed.sh

# Helpers
source .mise-tasks/utils/colors.sh
source .mise-tasks/utils/ask_yes_no.sh
