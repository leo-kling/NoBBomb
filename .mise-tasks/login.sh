#!/bin/bash
#MISE alias="login"
#MISE description="Login to Google Cloud and set up application default credentials"

source ./config.sh

gcloud auth login --project "$GCP_PROJECT_ID" --billing-project "$GCP_PROJECT_ID"


# Ensure Ressource Manager is up
gcloud services enable cloudresourcemanager.googleapis.com --project "$GCP_PROJECT_ID"
# Ensure Cloud Billing
gcloud services enable cloudbilling.googleapis.com --project "$GCP_PROJECT_ID"


gcloud auth application-default login --project "$GCP_PROJECT_ID" --billing-project "$GCP_PROJECT_ID" 
gcloud config set project "$GCP_PROJECT_ID"
gcloud config set billing/quota_project "$GCP_PROJECT_ID"

gcloud config list
