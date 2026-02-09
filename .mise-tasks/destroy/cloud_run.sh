#!/bin/bash
#MISE alias="destroy_cloud_run"
#MISE description="Destroy the Cloud Run component of NoBBomb. Use with caution, this is irreversible."

source .mise-tasks/utils/base_import.sh

# Destroy Cloud Run
print_color "blue" "Destroying Cloud Run service if it exists.."
if gcloud run services describe "$CLOUD_RUN_NAME" --project "$GCP_PROJECT_ID" --region "$DEPLOY_REGION" >/dev/null 2>&1; then
  gcloud run services delete "$CLOUD_RUN_NAME" --project "$GCP_PROJECT_ID" --region "$DEPLOY_REGION" --quiet
else
  print_color "yellow" "Cloud Run service '$CLOUD_RUN_NAME' not found; skipping."
fi
