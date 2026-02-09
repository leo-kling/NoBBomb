#!/bin/bash

# HARD CONFIG - DO NOT EDIT
export SCHEDULER_JOB_NAME="nobbomb-kill-switch-scheduler"
export SERVICE_ACCOUNT_NAME="nobbomb-kill-switch-sa"
export SERVICE_ACCOUNT_MAIL="$SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"
export CLOUD_RUN_NAME="nobbomb-kill-switch"
export BUDGET_ALERT_NAME="nobbomb-budget-alert-for-$GCP_PROJECT_ID"
export PUBSUB_BUDGET_ALERT_TOPIC="nobbomb-budget-alert-topic"
export DEPLOY_REGION="us-central1"
export EVENT_ARC="nobbomb-pubsub-to-cloudrun-event-arc"

# Services to enable
export GCP_SERVICES="artifactregistry.googleapis.com
  cloudbuild.googleapis.com run.googleapis.com
  cloudscheduler.googleapis.com
  billingbudgets.googleapis.com
  cloudbilling.googleapis.com
  eventarc.googleapis.com
  pubsub.googleapis.com"



# TESTS / Contributors Config
export FIRESTORE_TEST_DB="test-db-nobbomb"

# Budget Amount Calculations
export WEEKLY_BUDGET_AMOUNT=$(($MONTHLY_BUDGET_AMOUNT/4))
export DAILY_BUDGET_AMOUNT=$(($MONTHLY_BUDGET_AMOUNT/30))


# Under dev
# Alert on budget reached (string)
#   - DAILY    : Daily / Weekly / Monthly   => MONTHLY_BUDGET_AMOUNT / 30
#   - WEEKLY   : Weekly / Monthly           => MONTHLY_BUDGET_AMOUNT / 4
#   - MONTHLY  : Monthly                    => MONTHLY_BUDGET_AMOUNT
#   - NONE     : No Alert
export ALERT_ON_BUDGET_REACHED="MONTHLY"