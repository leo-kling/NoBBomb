"""Anti Burst Service Module."""

from typing import Any

from config.budget import ProjectBudget
from config.monitored_services_list import MONITORED_SERVICES
from helpers.constants import APP_LOGGER
from services.kill_switch import KillSwitchService
from wrappers.cloud_billing import CloudBillingWrapper
from wrappers.cloud_monitoring import WrapperCloudMonitoring


class NobbombAntiBurstService:
    """Nobbomb Anti Burst Service Class."""

    def __init__(
        self,
        cloud_billing_wrapper: CloudBillingWrapper,
        cloud_monitoring_wrapper: WrapperCloudMonitoring,
        kill_switch_service: KillSwitchService,
    ) -> None:
        """Initialize Nobbomb Anti Burst Service."""
        self.cloud_billing_wrapper = cloud_billing_wrapper
        self.cloud_monitoring_wrapper = cloud_monitoring_wrapper
        self.monitored_services_json_logs: list[dict[str, Any]] = []
        self.kill_switch_service = kill_switch_service
        APP_LOGGER.info(msg="Nobbomb Anti Burst Service initialized.")

    def run_anti_burst(self, project_budget: ProjectBudget) -> list[dict[str, Any]]:
        """Run NoBBomB Anti Burst."""

        APP_LOGGER.info(msg="Executing NoBBomB Anti Burst run...")

        for monitored_service in MONITORED_SERVICES:
            # Get Price pet unit for the monitored service
            APP_LOGGER.debug(msg="-" * 200)

            if monitored_service.populate_expense(
                cloud_billing_wrapper=self.cloud_billing_wrapper,
                cloud_monitoring_wrapper=self.cloud_monitoring_wrapper,
            ):
                APP_LOGGER.info(
                    msg=(
                        f"Successfully populated expense for "
                        f"{monitored_service.service_name}: "
                        f"{monitored_service.expense}"
                    )
                )
            else:
                APP_LOGGER.error(
                    msg=(
                        f"Failed to populate expense for "
                        f"{monitored_service.service_name}."
                    )
                )
                continue

            project_budget.current_expense.monthly += monitored_service.expense or 0.0
            self.monitored_services_json_logs.append(monitored_service.as_json())

        APP_LOGGER.info(msg=f"Current Expense: {project_budget.current_expense}")
        if project_budget.check_expense_limit():
            self.kill_switch_service.activate()
        return self.monitored_services_json_logs
