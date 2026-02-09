#!/bin/bash
#MISE alias="generate_bigquery_activities"
#MISE description="Generate BigQuery activities for testing purposes"

source .mise-tasks/utils/colors.sh

echo "Generating BigQuery activities..."
source .mise-tasks/utils/colors.sh

print_color "blue" "Running a sample BigQuery query to generate activity..."

bq query --use_legacy_sql=false \
    --project_id="${GCP_PROJECT_ID}" \
    'SELECT title, SUM(views) as v
    FROM `bigquery-public-data.wikipedia.pageviews_2023`
    TABLESAMPLE SYSTEM (1 PERCENT)
    WHERE datehour >= "2023-12-01"
    GROUP BY 1 ORDER BY 2 DESC LIMIT 10'

print_color "green" "BigQuery activity generation completed."