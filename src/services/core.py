"""Core Logic of Nobbomb Service."""

import base64
import json
from typing import Any

from fastapi import Request

from config.budget import ExpenseLimit, ProjectBudget
from helpers.constants import APP_LOGGER
from services.anti_burst import NobbombAntiBurstService
from services.kill_switch import KillSwitchService
from wrappers.cloud_billing import CloudBillingWrapper
from wrappers.cloud_monitoring import WrapperCloudMonitoring
from wrappers.ressource_manager import RessourceManagerWrapper


class NobbombCoreService:
    """Core Service for Nobbomb."""

    def __init__(self):
        """Initialize the core service."""
        self.cloud_billing_wrapper = CloudBillingWrapper()
        self.cloud_monitoring_wrapper = WrapperCloudMonitoring()
        self.expense_limit = ExpenseLimit()
        self.ressource_manager_wrapper = RessourceManagerWrapper()
        self.kill_switch_service = KillSwitchService(
            cloud_billing_wrapper=self.cloud_billing_wrapper,
            ressource_manager_wrapper=self.ressource_manager_wrapper,
        )

        APP_LOGGER.info("NobbombCoreService initialized.")

    def experimental_anti_burst(self) -> list[dict[str, Any]]:
        """Run all Nobbomb Anti Burst checks."""

        nobbomb_anti_burst_service = NobbombAntiBurstService(
            cloud_billing_wrapper=self.cloud_billing_wrapper,
            cloud_monitoring_wrapper=self.cloud_monitoring_wrapper,
            kill_switch_service=self.kill_switch_service,
        )

        APP_LOGGER.info(msg="Running Nobbomb core Anti Burst checks.")

        # EXPERIMENTAL : Check "Monitored Services" (Billing x Metrics)
        try:
            anti_burst_result = nobbomb_anti_burst_service.run_anti_burst(
                project_budget=ProjectBudget()
            )
        except Exception as err:
            APP_LOGGER.error(msg=f"Error during Nobbomb core Anti Burst checks: {err}")
            raise err

        APP_LOGGER.info(
            msg=f"Nobbomb core Anti Burst checks completed. Result: {anti_burst_result}"
        )
        return anti_burst_result

    async def check_budget_alert_status(self, request_from_event_arc: Request) -> bool:
        """Check budget alert from Event Arc."""
        do_trigger_kill_switch = False
        try:
            data_json = await request_from_event_arc.json()
            event_json = base64.b64decode(data_json["message"]["data"]).decode("utf-8")
            event_data = json.loads(event_json)
            cost_amount = event_data.get("costAmount")
            budget_amount = event_data.get("budgetAmount")
            APP_LOGGER.info(
                msg=f"Budget Alert Data: costAmount={cost_amount}, budgetAmount={budget_amount}"
            )
        except Exception as err:
            APP_LOGGER.error(
                msg=f"Error parsing budget alert data from Event Arc: {err}"
            )
            return False

        # Double check if cost_amount and budget_amount are present and valid
        if cost_amount is None or budget_amount is None:
            APP_LOGGER.error(
                msg="Cost amount or budget amount is missing in the event data. Cannot determine if kill switch should be triggered."
            )

        # Budget Not Reached
        if cost_amount < budget_amount:
            APP_LOGGER.info(
                msg="Cost amount is below the budget amount. Kill switch will not be triggered."
            )

        # Budget Reached or Exceeded
        if cost_amount >= budget_amount:
            APP_LOGGER.warning(
                msg="Cost amount has reached or exceeded the budget amount. Triggering kill switch."
            )
            do_trigger_kill_switch = True

        if do_trigger_kill_switch:
            self.kill_switch_service.activate()
            return True
        return False
