#!/bin/bash
#MISE alias="destroy_pub_sub"
#MISE description="Destroy the Pub/Sub component of NoBBomb. Use with caution, this is irreversible."

source .mise-tasks/utils/base_import.sh

# Destroy Pub Sub
print_color "blue" "Destroying Pub/Sub topic if it exists.."
if gcloud pubsub topics describe "$PUBSUB_BUDGET_ALERT_TOPIC" --project "$GCP_PROJECT_ID" >/dev/null 2>&1; then
  gcloud pubsub topics delete "$PUBSUB_BUDGET_ALERT_TOPIC" --project "$GCP_PROJECT_ID" --quiet
else
  print_color "yellow" "Pub/Sub topic '$PUBSUB_BUDGET_ALERT_TOPIC' not found; skipping."
fi
