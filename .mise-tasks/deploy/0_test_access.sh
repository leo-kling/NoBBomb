#!/bin/bash
#MISE alias="test_access"
#MISE description="Check GCP access and permissions"

tool_list=("gcloud")
for tool in "${tool_list[@]}"; do if command -v $tool >/dev/null 2>&1; then print_color "green" "$tool is installed"; else print_color "red" "$tool is NOT installed"; fi; done


print_color "blue" "Testing access to GCP project '$GCP_PROJECT_ID'..."

gcloud projects describe "$GCP_PROJECT_ID" >/dev/null 2>&1
if [ $? -ne 0 ]; then
    print_color "red" "Error: Unable to access GCP project '$GCP_PROJECT_ID'. Please check your GCP credentials and project ID."
    exit 1
else
    print_color "green" "Successfully accessed GCP project '$GCP_PROJECT_ID'."
fi

print_color "blue" "Checking Billing Account linked to GCP project '$GCP_PROJECT_ID'..."

BILLING_ACCOUNT=$(gcloud billing projects describe $GCP_PROJECT_ID \
    --format="value(billingAccountName)") || { print_color "red" "Error : Couldn't retrieve billing account"; exit 1; }

if [ -z "$BILLING_ACCOUNT" ]; then
    print_color "red" "Error: No billing account linked to project $GCP_PROJECT_ID";
    exit 1
fi

print_color "green" "Billing Account linked to project $GCP_PROJECT_ID: $BILLING_ACCOUNT"

echo ""

sleep 2