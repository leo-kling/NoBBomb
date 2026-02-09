#!/bin/bash
#MISE alias="destroy_event_arc"
#MISE description="Destroy the Event Arc component of NoBBomb. Use with caution, this is irreversible."

source .mise-tasks/utils/base_import.sh

# Destroy Event Arc
print_color "blue" "Destroying Event Arc trigger if it exists.."
if gcloud eventarc triggers describe "$EVENT_ARC" --project "$GCP_PROJECT_ID" --location "$DEPLOY_REGION" >/dev/null 2>&1; then
  gcloud eventarc triggers delete "$EVENT_ARC" --project "$GCP_PROJECT_ID" --location "$DEPLOY_REGION" --quiet
else
  print_color "yellow" "Event Arc trigger '$EVENT_ARC' not found; skipping."
fi
