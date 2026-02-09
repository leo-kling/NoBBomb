#!/bin/bash

source .mise-tasks/utils/base_import.sh

# Check Access gcloud / curl
source .mise-tasks/deploy/0_test_access.sh

# Load Variables
source .mise-tasks/variables/main.sh
source .mise-tasks/variables/computed.sh

# Show Configuration and Ask Confirmation
clear
print_color "green" "Checking configuration before deployment.."
source .mise-tasks/show.sh
ask_yes_no "Are all settings correct?"

# Double check : ARE YOU SURE ?
ask_yes_no "You're about to deploy NoBBomb. Do you want to proceed?"

print_color "blue" "Deploying NoBBomb components to project $GCP_PROJECT_ID .."

# Deploy Steps

# Enable Required Services
source .mise-tasks/deploy/1_services.sh

# Deploy Service Account and assign roles
source .mise-tasks/deploy/2_service_account.sh

# Deploy Cloud Run Service
source .mise-tasks/deploy/3_cloud_run.sh

# Deploy Cloud Scheduler if Anti Burst Feature is enabled
if [ "$EXPERIMENTAL_FEATURE" -eq 1 ]; then
    source .mise-tasks/deploy/4_cloud_scheduler.sh
fi

# Deploy Pub/Sub components (Kill Switch for Budget Alert)
source .mise-tasks/deploy/5_pub_sub.sh

# Deploy Budget Alert
source .mise-tasks/deploy/6_budget_alert.sh

# Deploy Event Arc
source .mise-tasks/deploy/7_event_arc.sh

# Final Message
print_color "blue" "Thanks a lot for using NoBBomb! Your project is now safer."
