"""Manage Google Cloud Monitoring interactions."""

from datetime import timedelta

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.services.metric_service.pagers import (
    ListTimeSeriesPager,
)

from helpers import utils
from helpers.constants import APP_LOGGER, PROJECT_ID


class WrapperCloudMonitoring:
    """Object to wrap Google Cloud Monitoring interactions."""

    def __init__(self) -> None:
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        APP_LOGGER.info(msg="Cloud Monitoring Wrapper initialized.")

    def get_numbers_of_units_in_time_series(
        self, metric_name: str, metric_filter: str | None, group_by_fields: list[str]
    ) -> int:
        """
        Extract the number of units from a Time Series object.
        """
        time_series = self.get_metrics_time_series(
            metric_name=metric_name,
            metric_filter=metric_filter,
            group_by_fields=group_by_fields,
        )
        if not time_series:
            return 0

        total_units = 0
        for ts in time_series:
            for point in ts.points:
                total_units += point.value.int64_value
        APP_LOGGER.debug(msg=f"Total units extracted from Time Series: {total_units}")
        return total_units

    def get_metrics_time_series(
        self, metric_name: str, metric_filter: str | None, group_by_fields: list[str]
    ) -> ListTimeSeriesPager | None:
        """
        Control any metrics from GCP and return a TimeSeries (TS).

        TS are aggregated by days.
        """

        # Time / Interval variables to build Cloud Monitoring Request
        time_interval: monitoring_v3.TimeInterval = monitoring_v3.TimeInterval(
            start_time=utils.first_day_of_current_month_midnight_utc(),
            end_time=utils.now_utc_datetime(),
        )

        APP_LOGGER.debug(
            msg=(
                f"Cloud Monitoring Request Filter: {metric_name} | "
                f"Time Interval: {time_interval}"
            )
        )

        # How to aggregate Cloud Monitoring Result
        aggregation = monitoring_v3.Aggregation(
            alignment_period=timedelta(days=1),
            per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_SUM,  # Align per SUM to have full value
            cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_SUM,
            group_by_fields=group_by_fields,
        )

        APP_LOGGER.debug(
            msg=(
                f"Cloud Monitoring Aggregation: "
                f"Alignment Period: {aggregation.alignment_period} | "
                f"Per Series Aligner: {aggregation.per_series_aligner} | "
                f"Cross Series Reducer: {aggregation.cross_series_reducer} | "
                f"Group By Fields: {aggregation.group_by_fields}"
            )
        )

        complete_metric_filter = f'metric.type = "{metric_name}"'
        if metric_filter:
            complete_metric_filter += f" AND {metric_filter}"

        time_series = self.monitoring_client.list_time_series(
            request={
                "name": f"projects/{PROJECT_ID}",
                "filter": complete_metric_filter,
                "interval": time_interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        APP_LOGGER.debug(
            msg=(
                f"Request for metric '{metric_name}' with filter '{complete_metric_filter}' returned "
            )
        )

        if time_series:
            APP_LOGGER.debug(msg=f"Time Series Data: {list(time_series)}")
            return time_series
        return None
