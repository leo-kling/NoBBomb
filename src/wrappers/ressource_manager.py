"""Manage Cloud Resource Manager interactions."""

from google.cloud import resourcemanager_v3

from helpers.constants import APP_LOGGER, PROJECT_ID


class RessourceManagerWrapper:
    """Object to wrap Cloud Resource Manager interactions."""

    def __init__(self) -> None:
        self.ressource_manager_client = resourcemanager_v3.ProjectsClient()

    def shutdown_the_project(self) -> None:
        """Shut down the Google Cloud project."""
        try:
            # Construct the request
            request = resourcemanager_v3.DeleteProjectRequest(
                name=f"projects/{PROJECT_ID}"
            )

            shutdown_operation = self.ressource_manager_client.delete_project(
                request=request
            )

            shutdown_response = shutdown_operation.result()

            APP_LOGGER.info(f"Shutdown operation result: {shutdown_response}")
            APP_LOGGER.critical(f"Project {PROJECT_ID} has been marked for deletion.")
        except Exception as e:
            APP_LOGGER.error(f"Error during project shutdown: {e}")
