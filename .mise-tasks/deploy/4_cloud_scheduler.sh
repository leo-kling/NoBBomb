#!/bin/bash
#MISE alias="create_cloud_scheduler"
#MISE description="Deploy Cloud Scheduler Job for triggering Cloud Run Job"

# Destroy
source .mise-tasks/destroy/cloud_scheduler.sh

if [ "$EXPERIMENTAL_FEATURE" -eq 1 ]; then
    print_color "blue" "Working on NoBBomb Cloud Scheduler Job.."
    echo ""

    # Get Cloud Run URL First
    CLOUD_RUN_URL=$(gcloud run services describe "$CLOUD_RUN_NAME" \
      --project "$GCP_PROJECT_ID" \
      --region "$DEPLOY_REGION" \
      --format='value(status.url)')

    echo "Cloud Run URL: $CLOUD_RUN_URL"

    # Create Cloud Scheduler Job
    gcloud scheduler jobs create http "$SCHEDULER_JOB_NAME" \
        --project "$GCP_PROJECT_ID" \
        --location "$DEPLOY_REGION" \
        --schedule "*/5 * * * *" \
        --uri "$CLOUD_RUN_URL/nobbomb" \
        --http-method POST \
        --oidc-service-account-email "$SERVICE_ACCOUNT_MAIL" \
        --max-retry-attempts 0

    echo ""
    print_color "blue" "Cloud Scheduler deployment is complete."
    echo ""
fi