#!/bin/bash
#MISE alias="destroy_cloud_scheduler"
#MISE description="Destroy the Cloud Scheduler component of NoBBomb. Use with caution, this is irreversible."

source .mise-tasks/utils/base_import.sh

# Destroy Cloud Scheduler
print_color "blue" "Destroying Cloud Scheduler if it exists..."
if gcloud scheduler jobs describe "$SCHEDULER_JOB_NAME" --project "$GCP_PROJECT_ID" --location "$DEPLOY_REGION" >/dev/null 2>&1; then
  gcloud scheduler jobs delete "$SCHEDULER_JOB_NAME" --project "$GCP_PROJECT_ID" --location "$DEPLOY_REGION" --quiet
else
  print_color "yellow" "Cloud Scheduler job '$SCHEDULER_JOB_NAME' not found; skipping."
fi