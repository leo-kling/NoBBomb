#!/bin/bash
#MISE alias="publish_fake_budget"
#MISE description="Send a fake budget alert to Pub/Sub to test the system (event arc => cloud run)."

source .mise-tasks/utils/base_import.sh

echo "Publishing a fake budget alert to Pub/Sub topic $PUBSUB_BUDGET_ALERT_TOPIC on project $GCP_PROJECT_ID"

read -r -n1 -p $'Choose a scenario:\n1) Expense > Budget\n2) Expense < Budget\nYour choice [1/2]: ' CHOICE
echo

case "$CHOICE" in
    1)
        MESSAGE_BODY='{
                "budgetDisplayName": "Fake Budget Alert",
                "costAmount": 180.321,
                "costIntervalStart": "2021-02-01T08:00:00Z",
                "budgetAmount": 152.557,
                "budgetAmountType": "SPECIFIED_AMOUNT",
                "alertThresholdExceeded": 0.9,
                "forecastThresholdExceeded": 0.2,
                "currencyCode":  "USD"
        }'
        ;;
    2)
        MESSAGE_BODY='{
                "budgetDisplayName": "Fake Budget Alert",
                "costAmount": 120.321,
                "costIntervalStart": "2021-02-01T08:00:00Z",
                "budgetAmount": 152.557,
                "budgetAmountType": "SPECIFIED_AMOUNT",
                "alertThresholdExceeded": 0.9,
                "forecastThresholdExceeded": 0.2,
                "currencyCode":  "USD"
        }'
        ;;
    *)
        echo "Invalid Choice. Please choose 1 or 2."
        exit 1
        ;;
esac

gcloud pubsub topics publish "$PUBSUB_BUDGET_ALERT_TOPIC" \
        --message="$MESSAGE_BODY"
