"""List Of NoBBomb Monitored Services Objects for ANTI BURST control."""

from typing import Any

from pydantic import BaseModel

from helpers.constants import APP_LOGGER
from wrappers.cloud_billing import CloudBillingWrapper
from wrappers.cloud_monitoring import WrapperCloudMonitoring


class MonitoredService(BaseModel):
    """Nobbomb Monitored Service Class."""

    service_name: str = ""
    service_id: str = ""
    sku_name: str = ""
    sku_id: str = ""
    # Cloud Billing
    price_tier: int = 0
    # Cloud Monitoring
    metric_name: str = ""
    metric_filter: str | None = None
    # Computed Fields
    price_per_unit: float | None = None
    number_of_units: int | None = None
    expense: float | None = None

    def populate_expense(
        self,
        cloud_billing_wrapper: CloudBillingWrapper,
        cloud_monitoring_wrapper: WrapperCloudMonitoring,
    ) -> bool:
        """Populate Expense Field."""
        try:
            self.get_monitored_service_price_per_unit(
                cloud_billing_wrapper=cloud_billing_wrapper
            )
        except Exception as error:
            APP_LOGGER.error(
                msg=(f"Error getting price per unit for {self.service_name}: {error}")
            )
            return False
        try:
            self.get_numbers_of_units_in_time_series(
                cloud_monitoring_wrapper=cloud_monitoring_wrapper
            )
        except Exception as error:
            APP_LOGGER.error(
                msg=(f"Error getting number of units for {self.service_name}: {error}")
            )
            return False
        if self.price_per_unit is not None and self.number_of_units is not None:
            self.expense = self.price_per_unit * self.number_of_units
            APP_LOGGER.debug(
                msg=(f"Expense for {self.service_name}: " f"{self.expense}")
            )
        return True

    def get_monitored_service_price_per_unit(
        self, cloud_billing_wrapper: CloudBillingWrapper
    ) -> None:
        """Get Price per unit."""
        self.price_per_unit = cloud_billing_wrapper.get_sku_price_per_unit(
            service_id=self.service_id,
            sku_id=self.sku_id,
            price_tier=self.price_tier,
        )
        APP_LOGGER.debug(
            msg=(f"Price per unit for {self.service_name}: " f"{self.price_per_unit}")
        )

    def get_numbers_of_units_in_time_series(
        self, cloud_monitoring_wrapper: WrapperCloudMonitoring
    ) -> None:
        """Get Count from Time Series."""
        self.number_of_units = (
            cloud_monitoring_wrapper.get_numbers_of_units_in_time_series(
                metric_name=self.metric_name,
                metric_filter=self.metric_filter,
                group_by_fields=[],
            )
        )
        APP_LOGGER.debug(
            msg=(f"Number of units for {self.service_name}: {self.number_of_units}")
        )

    def as_json(self) -> dict[str, Any]:
        """Return Monitored Service as JSON."""
        return self.model_dump()
