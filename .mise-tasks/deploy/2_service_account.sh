#!/bin/bash
#MISE alias="create_service_account"
#MISE description="Create a new service account in GCP + assign permissions"

print_color "blue" "Working on NoBBomb Service Account.."
echo ""

if gcloud iam service-accounts list \
    --project "$GCP_PROJECT_ID" \
    --filter "email=$SERVICE_ACCOUNT_MAIL" \
    --format "value(email)" | grep -q "$SERVICE_ACCOUNT_MAIL"; then
    print_color "green" "Service Account already exists: $SERVICE_ACCOUNT_MAIL, using it."
else
    print_color "yellow" "Service Account does not exist. Creating it.."
    gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
        --project "$GCP_PROJECT_ID" \
        --display-name "NoBBomb Kill Switch Service Account"
fi

# IAM Permissions
echo ""
print_color "blue" "Working on Service Account IAM Permissions.."
echo ""

# Add run invoker role
print_color "yellow" "Adding 'Cloud Run Invoker' role to the Service Account.."
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member "serviceAccount:$SERVICE_ACCOUNT_MAIL" \
    --role "roles/run.invoker" \
    --quiet \
    --condition None > /dev/null 2>&1

# Add monitoring viewer role
print_color "yellow" "Adding 'Monitoring Viewer' role to the Service Account.."
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member "serviceAccount:$SERVICE_ACCOUNT_MAIL" \
    --role "roles/monitoring.viewer" \
    --quiet \
    --condition None > /dev/null 2>&1

# Add monitoring viewer role
print_color "yellow" "Adding 'Service Usage Admin' role to the Service Account.."
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member "serviceAccount:$SERVICE_ACCOUNT_MAIL" \
    --role "roles/serviceusage.serviceUsageAdmin" \
    --quiet \
    --condition None > /dev/null 2>&1

# Add billing project manager role
print_color "yellow" "Adding 'Billing Project Manager' role to the Service Account.."
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member "serviceAccount:$SERVICE_ACCOUNT_MAIL" \
    --role "roles/billing.projectManager" \
    --quiet \
    --condition None > /dev/null 2>&1

# Add Project Deleter role
print_color "yellow" "Adding 'Project Deleter' role to the Service Account.."
gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" \
    --member "serviceAccount:$SERVICE_ACCOUNT_MAIL" \
    --role "roles/resourcemanager.projectDeleter" \
    --quiet \
    --condition None > /dev/null 2>&1

echo ""
print_color "blue" "Service Account setup is complete."
echo ""
