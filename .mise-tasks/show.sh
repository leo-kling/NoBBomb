#!/bin/bash
#MISE alias="show"
#MISE description="Check current configuration settings before deployment"

source .mise-tasks/utils/colors.sh

LABEL_WIDTH=20

if [ "$EXPERIMENTAL_FEATURE" == 1 ]; then
    EXPERIMENTAL_FEATURE_LABEL="Enabled"
else
    EXPERIMENTAL_FEATURE_LABEL="Disabled"
fi

if [ "$DEBUG_MODE" == 1 ]; then
    DEBUG_MODE_LABEL="DEBUG"
else
    DEBUG_MODE_LABEL="INFO"
fi

echo ""

echo -e "${BLUE}NoBBomb Settings:${RESET}"

echo -e "${YELLOW}Base${RESET}"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "GCP Project ID" "$GCP_PROJECT_ID"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Deploy Region" "$DEPLOY_REGION"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Billing Account ID" "$BILLING_ACCOUNT_ID"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Currency Code" "$CURRENCY_CODE"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Anti Burst Feature" "$EXPERIMENTAL_FEATURE_LABEL"


echo -e "${YELLOW}Budget${RESET}"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Monthly" "$MONTHLY_BUDGET_AMOUNT"
#printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Weekly" "$WEEKLY_BUDGET_AMOUNT"
#printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Daily" "$DAILY_BUDGET_AMOUNT"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Mail Alert" "When $ALERT_ON_BUDGET_REACHED is Reached"


echo -e "${YELLOW}Kill Switch${RESET}"
printf "%-${LABEL_WIDTH}s : ${RED}%s${RESET}\n" "Mode" "$ACTION_ON_BUDGET_REACHED"


echo -e "${YELLOW}Debug${RESET}"
printf "%-${LABEL_WIDTH}s : ${GREEN}%s${RESET}\n" "Level" "$DEBUG_MODE_LABEL"
echo ""
