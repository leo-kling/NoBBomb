"""Kill Switch Service Module."""

from helpers.constants import ACTION_ON_BUDGET_REACHED, APP_LOGGER
from wrappers.cloud_billing import CloudBillingWrapper
from wrappers.ressource_manager import RessourceManagerWrapper


class KillSwitchService:
    """
    Kill Switch Service Class to kill a GCP Project.

    DISABLE_BILLING: Disable Billing Account, this is brutal
    SHUTDOWN: Turn the Project off, recuperable before 30 days grace
    NONE: Done Nothing - Implement your own logic

    """

    def __init__(
        self,
        cloud_billing_wrapper: CloudBillingWrapper,
        ressource_manager_wrapper: RessourceManagerWrapper,
    ) -> None:
        """Initialize Kill Switch Service."""
        self.action_on_budget_reached = ACTION_ON_BUDGET_REACHED
        self.cloud_billing_wrapper = cloud_billing_wrapper
        self.ressource_manager_wrapper = ressource_manager_wrapper
        APP_LOGGER.info(
            msg=f"KillSwitchService initialized - Mode : {self.action_on_budget_reached}"
        )

    def activate(self) -> None:
        """
        Execute the Kill Switch action based on the configured mode.
        """
        match self.action_on_budget_reached:
            case "DISABLE_BILLING":
                self.disable_billing_project()
            case "SHUTDOWN":
                self.shutdown_project()
            case "NONE":
                self.none()
            case _:
                pass

    def disable_billing_project(self) -> None:
        """
        Disable billing for the GCP Project.

        SEE: https://docs.cloud.google.com/billing/docs/how-to/modify-project#disable_billing_for_a_project
        """
        self.cloud_billing_wrapper.disable_billing_for_the_project()

    def shutdown_project(self) -> None:
        """
        Shutdown the GCP Project.

        SEE: https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects
        """
        self.ressource_manager_wrapper.shutdown_the_project()

    def none(self) -> None:
        """
        No action taken

        Or implement your own logic here.
        """
        APP_LOGGER.info(msg="No action taken as per configuration.")
