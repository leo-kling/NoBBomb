# Note used.. yet?
"""Manage Cloud Budget resources."""

from google.cloud.billing import budgets_v1
from google.cloud.billing.budgets_v1.types import Budget

from helpers.constants import APP_LOGGER, BILLING_ACCOUNT_ID, BUDGET_ALERT_NAME


class CloudBudgetWrapper:
    """Wrapper for Google Cloud Budget API."""

    def __init__(self):
        self.client = budgets_v1.BudgetServiceClient()
        # Clean billing account ID
        self.billing_account_id = BILLING_ACCOUNT_ID.replace("billingAccounts/", "")
        self.display_name_target = BUDGET_ALERT_NAME
        APP_LOGGER.info("CloudBudgetWrapper initialized.")

    def check_budget_alert(self):
        """Get the current status of the budget alert."""

        parent = f"billingAccounts/{self.billing_account_id}"

        APP_LOGGER.info(
            f"Searching budget with display name: {self.display_name_target}"
        )

        target_budget: Budget | None = None
        for budget in self.client.list_budgets(parent=parent):
            if budget.display_name == self.display_name_target:
                target_budget = budget
                APP_LOGGER.info(
                    f"Found budget: {budget.display_name} with ID: {budget.name}"
                )
                break

        if not target_budget:
            APP_LOGGER.error(
                f"Budget '{self.display_name_target}' not found in account {self.billing_account_id}"
            )
            return None

        APP_LOGGER.debug(f"Budget details: {target_budget}")
        return True
