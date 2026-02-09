"""Utils module for various helper functions."""

from datetime import datetime, timezone


def first_day_of_current_month_midnight_utc() -> datetime:
    """
    Return the datetime of the first day of the current month at 00:00:00 UTC.
    """
    now = datetime.now(timezone.utc)
    return now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


def now_utc_datetime() -> datetime:
    """
    Return the current datetime in UTC.
    """
    return datetime.now(timezone.utc)
