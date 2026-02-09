#!/bin/bash
#MISE alias="enable_services_to_test"
#MISE description="Enable GCP services required to run tests"

source .mise-tasks/utils/colors.sh

print_color "blue" "Enabling required GCP services for generating activities..."

gcloud services enable \
  firestore.googleapis.com \
  bigquery.googleapis.com \
  aiplatform.googleapis.com \
  --project=${GCP_PROJECT_ID}
