#!/bin/bash

# Billing Account ID and Currency Code Detection
export BILLING_ACCOUNT_ID=$(gcloud billing projects describe "$GCP_PROJECT_ID" --format="value(billingAccountName)" | sed 's/.*\///')
export CURRENCY_CODE=$(gcloud billing accounts describe "$BILLING_ACCOUNT_ID" --format="value(currencyCode)")

# Auth Token Retrieval
#export CLOUD_TOKEN=$(gcloud auth print-access-token)
#export ADC_CLOUD_TOKEN=$(gcloud auth application-default print-access-token)

# GCP Project Number Retrieval
export GCP_PROJECT_NUMBER=$(gcloud projects describe "$GCP_PROJECT_ID" --format="value(projectNumber)")