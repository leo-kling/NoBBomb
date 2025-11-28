# NoBBomb

![Static Badge](https://img.shields.io/badge/state-alpha-f7f57c)
![Static Badge](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11%20|%203.12-00c914)
![Static Badge](https://img.shields.io/badge/contribution-closed-ff545d)
![Static Badge](https://img.shields.io/badge/code%20style-black-000000)
![Static Badge](https://img.shields.io/badge/linting-pylint-96981D)
[![Discord](https://img.shields.io/discord/1444015032252895275)](https://discord.gg/SgXCAQpTxy)


_Introducing No Billing Bomb (NoBBomb)._

**NoBBomb has a limited scope and won't protect you against every expense.**

This project is designed to protect you from unexpected cloud costs. It monitors the most vulnerable APIs, those most likely to trigger massive bills in a very short time. It is supposed to act as **GCP Kill Switch** to prevent _Billing Bomb_.

It leverages Cloud Monitoring and Logs to estimate certain API expenses, with an approximate lag of 5 minutes.

While the estimates are not perfectly precise, this tool may help you avoid catastrophic bills.

Do not forget to check [Limitations](https://github.com/leo-kling/NoBBomb?tab=readme-ov-file#limitations) and [Covered Services](https://github.com/leo-kling/NoBBomb?tab=readme-ov-file#covered-services) as the project is limited.

## Deploy

### Quick And Simple

First, clone this project on your computer.

Be sure to have `gcloud` CLI installed and then, with sufficient access on GCP (ex: _Owner_), run :

```bash
gcloud auth login && gcloud auth application-default login && sh deploy.sh
```

Anwser each question.

This will create/deploy everything you need to protect your project
with NoBBomb :

- Services
  - `artifactregistry.googleapis.com`
  - `cloudbuild.googleapis.com`
  - `run.googleapis.com`
  - `cloudscheduler.googleapis.com`
- Service Account
  - Named `nobbomb-kill-switch-sa@[GCP_PROJECT_ID].iam.gserviceaccount.com`
- IAM
  - `roles/run.invoker` on the Cloud Run
  - `roles/monitoring.viewer`
  - `roles/serviceusage.serviceUsageAdmin`
- Cloud Run ([Job](https://console.cloud.google.com/run/jobs?))
  - Named `nobbomb-kill-switch`
- Cloud Scheduler (At every 30th minute)
  - Named `nobbomb-kill-switch-scheduler`

The region is hard set to `us-central1` for the moment. It should have no impact on the app.

### Custom Deployment

If you're more comfortable using the GCP Console (UI), you can create a Cloud Run service directly from the Docker image.
Note that you'll still need to create and configure the service account and Cloud Scheduler job yourself.

Alternatively, you can simply clone this repository and customize it however you like.

# Limitation(s)

## General

The code base is currently under active development and may undergo significant changes.

Our goal is to help as many people as possible, especially small businesses, students, and non-critical projects (dev environment, sandbox).

Before using NoBBomb, please read the documentation below to understand how it works and which services are covered.

## Known Technical Issues

- Some parts of the code may be repeated (not DRY)
- The project’s structure could probably be better organized
- Unit tests are missing and should be added
- GCP pricing should be loaded from a hosted JSON to avoid rebuilding when prices change
- The Makefile isn’t using the virtual environment correctly
- The project needs a clearer roadmap for next steps
- Role `roles/serviceusage.serviceUsageAdmin` is overkill
- The app cannot determine whether a service is free-tier or paid
- Expenses are currently limited to USD only

## Ignoring Cloud Billing

**NoBBomb does NOT monitor Cloud Billing.** The app acts as a _safeguard_ for specific APIs that may unexpectedly spike and create a Billing Bomb.

This means you **still need** to set up a Budget Alarm to monitor your project. NoBBomb will only help by shutting down the specific APIs you designate if they start consuming too many resources.

## Unstoppable Cost

Some costs cannot be avoided. For example, if you run an inefficient BigQuery query on public data that consumes terabytes of data, you are knowingly executing a query that will incur significant charges.

NoBBomb may detect the high cost afterward and prevent you from running another query, but what has already been executed cannot be undone.

## Update lag

Some monitored metrics (ex: Gemini Price) may change due to updates by Google, which can take time to be reflected. You may need to update NoBBomb accordingly. Since this is a known issue, I plan to use external data to manage the price list, so you won’t have to update the app regularly.

## Self Costs

The app consumes some Cloud Monitoring API calls and time series, as mentioned in [Cloud Monitoring pricing summary](https://cloud.google.com/stackdriver/pricing#monitoring-pricing-summary). Although there is a relatively large free tier, excessive usage of the app may still generate costs.

# Covered Services

For now, each service listed here will be shut down by the app if the `NUKE_MODE` environment variable is enabled.

- **aiplatform.googleapis.com**
  - Input (text, image, video) & Output (response and reasoning)
    - gemini-3-pro\*
    - gemini-2.5-pro\*
    - gemini-2.5-flash\*
    - gemini-2.0-flash\*
  - Embedding
    - gemini-embedding-001
  - Image Generation
    - gemini-3-pro-image-preview
    - gemini-2.5-flash-image
    - imagen-4.0\*
    - imagen-3.0-generate-002
  - TTS
    - gemini-2.5-pro-preview-tts
    - gemini-2.5-flash-preview-tts
  - Native Audio
    - gemini-2.5-flash-native-audio-preview-09-2025
- **bigquery.googleapis.com**
  - Query Billable Bytes
    - Query Job
- **firestore.googleapis.com**
  - Read
  - Write
  - Delete
  - TTL Delete

# How It Works

- Collects time series data from Cloud Monitoring
- Estimates spending using the GCP price list
- If `NUKE_MODE` is enabled, disables affected APIs, which terminates the corresponding services and resources

# Prerequisites

## IAM Permissions

If you're not fully familiar with the process, simply being the project owner is more than enough when using the deploy script.

However, if you know the platform well, feel free to configure and build the project in whatever way best suits your needs.

## Running Locally

Note that the app is intended to run on Cloud Run, local runs should remain occasional.

Be sure to:

- Export Env Variables in your terminal / Write your own `.env` file
- Run `gcloud auth application-default login`
- Ensure you have the required IAM permissions

Then, you can run the script using :

```bash
GCP_PROJECT_ID=YOUR_GCP_PROJECT_ID python src/main.py
```

## Running on Cloud Run / GCP

- Use a Service Account with the necessary IAM roles
- Set the correct environment variables

## Environment Variables

| Variable Name         | Mandatory | Default Value | Description |
| --------------------- | --------- | ------------- |---------------------------|
| GCP_PROJECT_ID        | ✅        | ❌            | Your GCP Project ID       |
| DAILY_EXPENSE_LIMIT   | ❌        | 100           | Past 24 hours             |
| WEEKLY_EXPENSE_LIMIT  | ❌        | 500           | Past 7 days               | 
| MONTHLY_EXPENSE_LIMIT | ❌        | 1000          | Past 30 days              |
| DEBUG_MODE            | ❌        | `False`       | Verbose mode              |
| NUKE_MODE             | ❌        | `False`       | [Disable Services API](https://docs.cloud.google.com/service-usage/docs/enable-disable#disabling)|

Note that if `NUKE_MODE` is enabled, any budget reached will disable every API listed by NoBBomb.

Also, using `sh deploy` won't use any Default Value as you're requested to fill them.

# License

This project is licensed under the terms of the MIT license.
