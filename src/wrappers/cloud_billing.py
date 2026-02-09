"""Manage Google Cloud Billing interactions."""

from typing import Any

from google.api_core import exceptions
from google.cloud import billing_v1
from google.cloud.billing_v1 import CloudBillingClient, CloudCatalogClient
from google.cloud.billing_v1.services.cloud_catalog.pagers import ListSkusPager
from google.cloud.billing_v1.types import ProjectBillingInfo, Sku
from google.cloud.billing_v1.types.cloud_billing import UpdateProjectBillingInfoRequest

from helpers.constants import (
    APP_LOGGER,
    BILLING_ACCOUNT_ID,
    BUDGET_ALERT_NAME,
    CURRENCY_CODE,
    PROJECT_ID,
)


class CloudBillingWrapper:
    """Object to wrap Google Cloud Billing interactions."""

    def __init__(self) -> None:
        # SKUs Part
        self.cloud_catalog_client = CloudCatalogClient()
        self.skus_dict: dict[str, dict[str, Any]] = {}
        # Billing Alert Part
        self.billing_client: CloudBillingClient = billing_v1.CloudBillingClient()
        self.billing_account_id = BILLING_ACCOUNT_ID.replace("billingAccounts/", "")
        self.display_name_target = BUDGET_ALERT_NAME
        APP_LOGGER.debug(msg="CloudBillingWrapper initialized.")

    def get_sku_price_per_unit(
        self, service_id: str, sku_id: str, price_tier: int
    ) -> float | None:
        """
        Get the price per unit for a given SKU ID under a given service ID.
        """
        APP_LOGGER.info(
            msg=f"Retrieving price per unit for SKU ID {sku_id} under service ID {service_id}..."
        )
        self.populate_skus_per_service(service_id=service_id)
        return self.get_price_per_unit_from_sku(
            service_id=service_id, sku_id=sku_id, price_tier=price_tier
        )

    def populate_skus_per_service(self, service_id: str) -> ListSkusPager | None:
        """
        Get SKU for a given GCP service.

        see: https://cloud.google.com/skus
        """
        if service_id in self.skus_dict:
            return

        self.skus_dict[service_id] = {}

        sku: Sku
        for sku in self.cloud_catalog_client.list_skus(
            request={"parent": f"services/{service_id}", "currency_code": CURRENCY_CODE}
        ):
            self.skus_dict[service_id][sku.sku_id] = sku
            APP_LOGGER.debug(
                msg=f"SKU ID {sku.sku_id} added under service ID {service_id}."
            )

    def get_price_per_unit_from_sku(
        self, service_id: str, sku_id: str, price_tier: int
    ) -> float | None:
        """
        Extract price per unit from SKU object and normalize it to the base unit (e.g., Bytes).
        """

        if service_id in self.skus_dict and sku_id in self.skus_dict[service_id]:
            sku: Sku = self.skus_dict[service_id][sku_id]

            if not sku.pricing_info:
                return None

            pricing_info = sku.pricing_info[0]
            pricing_expression = pricing_info.pricing_expression

            if pricing_expression and pricing_expression.tiered_rates:
                # 1. Get the price for the usage_unit (e.g., price per 1 TiB)
                tiered_rate = pricing_expression.tiered_rates[price_tier]
                price_per_usage_unit = (
                    tiered_rate.unit_price.nanos / 1e9 + tiered_rate.unit_price.units
                )

                # 2. Get the conversion factor (e.g., how many bytes in 1 TiB)
                # If the factor is 0 or 1, it means the usage_unit is the base_unit
                conversion_factor = pricing_expression.base_unit_conversion_factor or 1

                # 3. Calculate price per base unit (e.g., price per 1 Byte)
                price_per_base_unit = price_per_usage_unit / conversion_factor

                APP_LOGGER.debug(
                    msg=f"SKU {sku_id}: {price_per_usage_unit} {CURRENCY_CODE} per {pricing_expression.usage_unit_description}. "
                    f"Converted to {price_per_base_unit} per {pricing_expression.base_unit_description}."
                )

                return price_per_base_unit
        return None

    def disable_billing_for_the_project(self) -> None:
        """Disable billing for a project by removing its billing account.

        Based on: https://docs.cloud.google.com/billing/docs/how-to/disable-billing-with-notifications#create-cloud-run-function
        """

        resource_name = f"projects/{PROJECT_ID}"

        project_billing_info = billing_v1.ProjectBillingInfo(
            billing_account_name=""  # No Billing Account
        )

        APP_LOGGER.debug(msg=f"Project Billing Info to update: {project_billing_info}")

        request = UpdateProjectBillingInfoRequest(
            name=resource_name, project_billing_info=project_billing_info
        )

        try:
            response: ProjectBillingInfo = (
                self.billing_client.update_project_billing_info(request=request)
            )
            APP_LOGGER.info(msg=f"Disable billing response: {response}")
            APP_LOGGER.critical(msg=f"Billing disabled for project {PROJECT_ID}.")
        except exceptions.PermissionDenied:
            APP_LOGGER.error(msg="Failed to disable billing, check permissions.")
