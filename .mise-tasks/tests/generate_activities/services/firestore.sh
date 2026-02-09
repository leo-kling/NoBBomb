#!/bin/bash
#MISE alias="generate_firestore_activities"
#MISE description="Generate Firestore activities for testing purposes"

source .mise-tasks/utils/colors.sh

print_color "blue" "Generating Firestore activities..."

# Cloud Token
CLOUD_TOKEN=$(gcloud auth print-access-token)

# Check if the test database exists; if not, create it
EXISTING_DB=$(gcloud firestore databases list --project=${GCP_PROJECT_ID} --format="value(name)" | grep -w "projects/${GCP_PROJECT_ID}/databases/${FIRESTORE_TEST_DB}")

if [ -z "$EXISTING_DB" ]; then
    print_color "yellow" "The database ${FIRESTORE_TEST_DB} does not exist. Creating it..."
    gcloud firestore databases create \
        --database="${FIRESTORE_TEST_DB}" \
        --location=${DEPLOY_REGION} \
        --type=firestore-native \
        --project=${GCP_PROJECT_ID}
else
    print_color "yellow" "The Base ${FIRESTORE_TEST_DB} already exists. Moving to the next step."
fi

# Enable TTL (essential for auto-deletion)
print_color "blue" "Configuring TTL on the 'expire_at' field for database ${FIRESTORE_TEST_DB}..."
print_color "yellow" "If it's the first time, it may be long, please be patient..."
echo ""

gcloud firestore fields ttls update expire_at \
    --collection-group="${FIRESTORE_TEST_DB}" \
    --enable-ttl \
    --database="${FIRESTORE_TEST_DB}" \
    --project=${GCP_PROJECT_ID}

# Calculate expiry time 2 minutes from now
EXPIRY_TIME=$(date -u -v+120s +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "+120 seconds" +"%Y-%m-%dT%H:%M:%SZ")

TOTAL_DOCS=1000
DELETE_COUNT=500
BATCH_SIZE=50

# --- 1. CREATE (1000 documents) ---
echo ""
print_color "blue" "Step 1/3: Creating $TOTAL_DOCS documents..."
for i in $(seq 1 $TOTAL_DOCS); do
  curl -sS -X POST -H "Authorization: Bearer $CLOUD_TOKEN" \
       -H "Content-Type: application/json" \
       --data "{\"fields\": {\"expire_at\": {\"timestampValue\": \"$EXPIRY_TIME\"}, \"val\": {\"integerValue\": \"$i\"}}}" \
       "https://firestore.googleapis.com/v1/projects/${GCP_PROJECT_ID}/databases/${FIRESTORE_TEST_DB}/documents/${FIRESTORE_TEST_DB}?documentId=doc_$i" \
       -o /dev/null &

  if [[ $((i % BATCH_SIZE)) -eq 0 ]]; then
    wait
    percent=$(( i * 100 / TOTAL_DOCS ))
    printf "\r[CREATE] Progress: [%-20s] %d%% (%d/%d)" "$(printf '#%.0s' $(seq 1 $((i/50))))" "$percent" "$i" "$TOTAL_DOCS"
  fi
done
wait
print_color "green" "\nCreation completed.\n"

# --- 2. READ (1000 documents) ---
print_color "blue" "Step 2/3: Reading $TOTAL_DOCS documents..."
for i in $(seq 1 $TOTAL_DOCS); do
  curl -sS -X GET -H "Authorization: Bearer $CLOUD_TOKEN" \
       "https://firestore.googleapis.com/v1/projects/${GCP_PROJECT_ID}/databases/${FIRESTORE_TEST_DB}/documents/${FIRESTORE_TEST_DB}/doc_$i" \
       -o /dev/null &

  if [[ $((i % BATCH_SIZE)) -eq 0 ]]; then
    wait
    percent=$(( i * 100 / TOTAL_DOCS ))
    printf "\r[READ]   Progress: [%-20s] %d%% (%d/%d)" "$(printf '#%.0s' $(seq 1 $((i/50))))" "$percent" "$i" "$TOTAL_DOCS"
  fi
done
wait
print_color "green" "\nRead completed.\n"

# --- 3. DELETE (500 documents) ---
print_color "blue" "Step 3/3: Deleting $DELETE_COUNT documents... (Leaving room for TTL Delete)"
for i in $(seq 1 $DELETE_COUNT); do
  curl -sS -X DELETE -H "Authorization: Bearer $CLOUD_TOKEN" \
       "https://firestore.googleapis.com/v1/projects/${GCP_PROJECT_ID}/databases/${FIRESTORE_TEST_DB}/documents/${FIRESTORE_TEST_DB}/doc_$i" \
       -o /dev/null &

  if [[ $((i % BATCH_SIZE)) -eq 0 ]]; then
    wait
    percent=$(( i * 100 / DELETE_COUNT ))
    printf "\r[DELETE] Progress: [%-20s] %d%% (%d/%d)" "$(printf '#%.0s' $(seq 1 $((i/25))))" "$percent" "$i" "$DELETE_COUNT"
  fi
done
wait
print_color "yellow" "\nCleanup completed."

print_color "green" "Firestore activity generation completed."