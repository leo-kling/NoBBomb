#!/bin/bash
#MISE alias="create_budget_alerts"
#MISE description="Create Budget Alerts for the project"

# Destroy
source .mise-tasks/destroy/budget_alert.sh

print_color "blue" "Working on Budget Alerts.."

PUBSUB_TOPIC_FULL_NAME="projects/$GCP_PROJECT_ID/topics/$PUBSUB_BUDGET_ALERT_TOPIC"

if gcloud billing budgets create \
    --project="$GCP_PROJECT_ID" \
    --billing-account="$BILLING_ACCOUNT_ID" \
    --display-name="$BUDGET_ALERT_NAME" \
    --budget-amount="${MONTHLY_BUDGET_AMOUNT}${CURRENCY_CODE}" \
    --calendar-period="month" \
    --threshold-rule="percent=0.75,basis=current-spend" \
    --threshold-rule="percent=0.9,basis=current-spend" \
    --threshold-rule="percent=1.0,basis=current-spend" \
    --filter-projects="projects/$GCP_PROJECT_ID" \
    --notifications-rule-pubsub-topic="$PUBSUB_TOPIC_FULL_NAME" \
    #--enable-project-level-recipients; # => Work in curl but not gcloud ?
then
  print_color "green" "Budget '$BUDGET_ALERT_NAME' created successfully."
else
  print_color "red" "Failed to create budget."
fi
