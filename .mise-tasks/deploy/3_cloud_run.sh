#!/bin/bash
#MISE alias="create_cloud_run"
#MISE description="Build and deploy to Cloud Run"

# Destroy
source .mise-tasks/destroy/cloud_run.sh

# Deploy Cloud Run Service
print_color "blue" "Working on NoBBomb Cloud Run Service.."
echo ""

gcloud run deploy $CLOUD_RUN_NAME \
    --project "$GCP_PROJECT_ID" \
    --source . \
    --region $DEPLOY_REGION \
    --set-env-vars GCP_PROJECT_ID="$GCP_PROJECT_ID" \
    --set-env-vars MONTHLY_BUDGET_AMOUNT="$MONTHLY_BUDGET_AMOUNT" \
    --set-env-vars WEEKLY_BUDGET_AMOUNT="$WEEKLY_BUDGET_AMOUNT" \
    --set-env-vars DAILY_BUDGET_AMOUNT="$DAILY_BUDGET_AMOUNT" \
    --set-env-vars ACTION_ON_BUDGET_REACHED="$ACTION_ON_BUDGET_REACHED" \
    --set-env-vars ALERT_ON_BUDGET_REACHED="$ALERT_ON_BUDGET_REACHED" \
    --set-env-vars DEBUG_MODE="$DEBUG_MODE" \
    --set-env-vars CURRENCY_CODE="$CURRENCY_CODE" \
    --set-env-vars BILLING_ACCOUNT_ID="$BILLING_ACCOUNT_ID" \
    --set-env-vars BUDGET_ALERT_NAME="$BUDGET_ALERT_NAME" \
    --service-account $SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com \
    --no-allow-unauthenticated

echo ""
print_color "blue" "Cloud Run Service deployment is complete."
echo ""