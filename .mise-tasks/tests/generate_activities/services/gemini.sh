#!/bin/bash
#MISE alias="generate_gemini_activities"
#MISE description="Generate Gemini activities for testing purposes"

source .mise-tasks/utils/colors.sh

print_color "blue" "Generating Gemini activities..."

# Get the current project ID
project_id=$(gcloud config get-value project)
location="us-central1"
access_token=$(gcloud auth print-access-token)

# Filter for Gemini models. 
# Note: This list might include embedding models which require a different API payload.
models=$(gcloud ai model-garden models list --model-filter=gemini --format="value(MODEL_ID,CAN_PREDICT)" | awk '$2=="Yes" {print $1}')

print_color "yellow" "Found the following predictable models:"
echo "$models"

if [ -z "$models" ]; then
    print_color "red" "No predictable models found."
    exit 1
fi

print_color "green" "Starting activity generation..."

for raw_model in $models; do
    # 1. Clean the model ID
    # The list command returns 'google/gemini-1.5-pro@default', but the API expects 'gemini-1.5-pro'
    # We strip 'google/' prefix and everything after '@'
    model_name=$(echo "$raw_model" | sed 's/^google\///' | sed 's/@.*//')
    
    # Skip embedding models as they use a different API endpoint (:embedContent)
    if [[ "$model_name" == *"embedding"* ]]; then
        print_color "yellow" "Skipping embedding model: $model_name (requires different API payload)"
        continue
    fi

    print_color "yellow" "Targeting model: $model_name"

    # 2. Send request via curl using the generateContent API
    # Gemini models use the 'publishers/google/models/{model}:generateContent' endpoint
    response=$(curl -s -X POST \
        -H "Authorization: Bearer $access_token" \
        -H "Content-Type: application/json" \
        "https://${location}-aiplatform.googleapis.com/v1/projects/${project_id}/locations/${location}/publishers/google/models/${model_name}:generateContent" \
        -d '{
            "contents": {
                "role": "user",
                "parts": { "text": "Generate the longest text possible." }
            },
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 10000
            }
        }')

    # Check if curl failed (exit code) or if the response contains an error JSON
    if [ $? -eq 0 ] && [[ "$response" != *"error"* ]]; then
        print_color "green" "Successfully generated activity for $model_name"
    else
        print_color "red" "Failed to contact $model_name"
        # Optional: Print the error response for debugging
        # echo "$response"
    fi
done

print_color "green" "Done."