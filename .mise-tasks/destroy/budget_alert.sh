#!/bin/bash
#MISE alias="destroy_budget_alert"
#MISE description="Destroy the Budget Alert component of NoBBomb. Use with caution, this is irreversible."

source .mise-tasks/utils/base_import.sh

# Destroy Budget Alert(s)
print_color "blue" "Destroying Budget Alert(s) if they exist..."
gcloud billing budgets list --billing-account "$BILLING_ACCOUNT_ID" --format="value(name)" --filter="displayName:$BUDGET_ALERT_NAME" | \
  awk -F/ '{print $NF}' | while read -r BUDGET_ID; do
    if [ -n "$BUDGET_ID" ]; then
      gcloud billing budgets delete "$BUDGET_ID" --billing-account "$BILLING_ACCOUNT_ID" --quiet
    fi
  done

if [ "${PIPESTATUS[0]}" -ne 0 ]; then
  print_color "yellow" "Budget '$BUDGET_ALERT_NAME' not found; skipping."
fi