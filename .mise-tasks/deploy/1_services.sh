#!/bin/bash
#MISE alias="enable_services"
#MISE description="Enable required GCP services for NoBBomb"

print_color "blue" "Working on NoBBomb Required Services.."

FIRST_LAUNCH=0

for SERVICE in $GCP_SERVICES; do
    echo ""
    print_color "blue" "Checking $SERVICE.."

    if ! gcloud services list --enabled \
        --filter="config.name=$SERVICE" \
        --project "$GCP_PROJECT_ID" \
        --format="value(config.name)" | grep -q "^$SERVICE$"; then

        print_color "blue" "$SERVICE is not enabled. Enabling now.."
        FIRST_LAUNCH=1

        gcloud services enable "$SERVICE" --project "$GCP_PROJECT_ID"

        until gcloud services list --enabled \
            --filter="config.name=$SERVICE" \
            --project "$GCP_PROJECT_ID" \
            --format="value(config.name)" | grep -q "^$SERVICE$"; do
            print_color "yellow" "Waiting for $SERVICE to be enabled.."
            sleep 5
        done

        print_color "green" "$SERVICE is now enabled"
    else
        print_color "green" "$SERVICE is already enabled"
    fi
done

if [ "$FIRST_LAUNCH" -eq 1 ]; then
    echo ""
    print_color "blue" "First launch detected. Waiting 2 minutes to ensure all services are fully deployed.."

    duration=120
    interval=2 
    total_steps=$((duration / interval))

    echo -n "Progress: ["
    for ((i=0; i<=total_steps; i++)); do
        sleep $interval
        percent=$(( i * 100 / total_steps ))
        num_hash=$(( i * 50 / total_steps ))
        num_dash=$(( 50 - num_hash ))

        echo -ne "\rProgress: ["
        for ((j=0; j<num_hash; j++)); do echo -n "#"; done
        for ((j=0; j<num_dash; j++)); do echo -n "-"; done
        echo -n "] $percent%"
    done
fi

echo ""
print_color "blue" "GCP Services are ready for NoBBomb deployment !"
echo ""
