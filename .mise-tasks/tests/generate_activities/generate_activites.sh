#!/bin/bash
#MISE alias="generate_activities"
#MISE description="Create some activites on GCP to test Metrics"

source .mise-tasks/variables/main.sh
source .mise-tasks/variables/computed.sh
source .mise-tasks/utils/ask_yes_no.sh

ask_yes_no "Generating activities on ${GCP_PROJECT_ID} ?"

# Enable Contributor required services
source .mise-tasks/tests/generate_activities/enable_services_to_test.sh

# Generate activities
source .mise-tasks/tests/generate_activities/services/firestore.sh
source .mise-tasks/tests/generate_activities/services/bigquery.sh
source .mise-tasks/tests/generate_activities/services/gemini.sh