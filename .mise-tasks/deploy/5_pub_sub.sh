#!/bin/bash
#MISE alias="create_pub_sub"
#MISE description="Create Pub/Sub topic for budget alerts"

# Destroy
source .mise-tasks/destroy/pub_sub.sh

print_color "blue" "Working on Pub/Sub topic for budget alerts.."
echo ""

if [ -z "$BILLING_ACCOUNT_ID" ]; then
  print_color "red" "Error: No billing account linked to project $GCP_PROJECT_ID"
  exit 1
fi

# Create Pub/Sub topic
print_color "blue" "Creating Pub/Sub topic '$PUBSUB_BUDGET_ALERT_TOPIC'..."

if gcloud pubsub topics describe "$PUBSUB_BUDGET_ALERT_TOPIC" --project="$GCP_PROJECT_ID" &>/dev/null; then
  print_color "blue" "Topic '$PUBSUB_BUDGET_ALERT_TOPIC' already exists. Renewing it by deleting and recreating..."
  gcloud pubsub topics delete "$PUBSUB_BUDGET_ALERT_TOPIC" --project="$GCP_PROJECT_ID" --quiet
fi

gcloud pubsub topics create "$PUBSUB_BUDGET_ALERT_TOPIC" --project="$GCP_PROJECT_ID" --message-retention-duration="7d"
print_color "green" "Topic '$PUBSUB_BUDGET_ALERT_TOPIC' created successfully."
