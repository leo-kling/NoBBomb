#!/bin/bash

# Your GCP Project ID (string)
export GCP_PROJECT_ID="YOUR_PROJECT_ID"

# Budget Value (integer)
# Using Project Default Currency CODE
export MONTHLY_BUDGET_AMOUNT=100

# Experimental Cloud Run (boolean)
# If you want to use the Cloud Run Anti Burst feature
# Saying no will disable the Scheduler, the kill switch is still active
#   - 1: Active, 0: Inactive
export EXPERIMENTAL_FEATURE=1

# Action settings (string)
#   -  DISABLE_BILLING  : Remove Billing Account (see: https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications)
#   -  SHUTDOWN         : Shutdown Project (see: https://support.google.com/googleapi/answer/6251787?hl=en#zippy=%2Cshut-down-a-project)
#   -  NONE             : Do nothing
export ACTION_ON_BUDGET_REACHED="DISABLE_BILLING"

# Debugger settings (boolean)
#   - 1: Active (verbose), 0: Inactive
export DEBUG_MODE=0