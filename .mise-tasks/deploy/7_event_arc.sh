#!/bin/bash
#MISE alias="create_event_arc"
#MISE description="Create Event Arc for the project"


# Destroy
source .mise-tasks/destroy/event_arc.sh

gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member="serviceAccount:service-$GCP_PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountTokenCreator"

gcloud eventarc triggers create "$EVENT_ARC" \
    --location="$DEPLOY_REGION" \
    --service-account="$SERVICE_ACCOUNT_MAIL" \
        --transport-topic="projects/$GCP_PROJECT_ID/topics/$PUBSUB_BUDGET_ALERT_TOPIC" \
        --destination-run-service="$CLOUD_RUN_NAME" \
        --destination-run-region="$DEPLOY_REGION" \
        --destination-run-path="/kill_switch" \
        --event-filters="type=google.cloud.pubsub.topic.v1.messagePublished"
