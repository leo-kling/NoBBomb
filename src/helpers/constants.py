"""Manage all constants / shared ressources."""

import os
from typing import Any

from helpers.logger import GCPLogger

# Generic Global Env Variables
TRUE_VALUES = ("true", "1", "yes")

# Debug Mode / Level for the Logger
DEBUG_MODE = os.environ.get("DEBUG_MODE", default="False").lower() in TRUE_VALUES
APP_LOGGER = GCPLogger(debug=DEBUG_MODE)
APP_LOGGER.info(msg="Debugger Up&Ready!")

# GCP Project ID (name) | Raise if not set
PROJECT_ID = os.environ["GCP_PROJECT_ID"]
APP_LOGGER.debug(msg=f"GCP Project ID: {PROJECT_ID}")

# Budget Constants
monthly_budget_amount = os.environ.get("MONTHLY_BUDGET_AMOUNT")
weekly_budget_amount = os.environ.get("WEEKLY_BUDGET_AMOUNT")
daily_budget_amount = os.environ.get("DAILY_BUDGET_AMOUNT")
if not monthly_budget_amount or not weekly_budget_amount or not daily_budget_amount:
    raise ValueError(
        "MONTHLY_BUDGET_AMOUNT, WEEKLY_BUDGET_AMOUNT, and DAILY_BUDGET_AMOUNT "
        "must be set in environment variables."
    )

MONTHLY_BUDGET_AMOUNT = int(monthly_budget_amount)
WEEKLY_BUDGET_AMOUNT = int(weekly_budget_amount)
DAILY_BUDGET_AMOUNT = int(daily_budget_amount)

# Currency Code
CURRENCY_CODE = os.environ.get("CURRENCY_CODE")
if not CURRENCY_CODE:
    raise ValueError("CURRENCY_CODE must be set in environment variables.")

# Action On Budget Reached
ACTION_ALLOWED_VALUES = {"DISABLE_BILLING", "SHUTDOWN", "NONE"}
ACTION_ON_BUDGET_REACHED = os.environ.get("ACTION_ON_BUDGET_REACHED")
if ACTION_ON_BUDGET_REACHED not in ACTION_ALLOWED_VALUES:
    raise ValueError(
        f"ACTION_ON_BUDGET_REACHED must be one of {ACTION_ALLOWED_VALUES}, "
        f"got '{ACTION_ON_BUDGET_REACHED}'"
    )

# Alert On Budget Reached
ALERT_ALLOWED_VALUES = {"MONTHLY", "WEEKLY", "DAILY", "NONE"}
ALERT_ON_BUDGET_REACHED = os.environ.get("ALERT_ON_BUDGET_REACHED")
if ALERT_ON_BUDGET_REACHED not in ALERT_ALLOWED_VALUES:
    raise ValueError(
        f"ALERT_ON_BUDGET_REACHED must be one of {ALERT_ALLOWED_VALUES}, "
        f"got '{ALERT_ON_BUDGET_REACHED}'"
    )

# Billing Account ID
BILLING_ACCOUNT_ID = os.environ.get("BILLING_ACCOUNT_ID")
if not BILLING_ACCOUNT_ID:
    raise ValueError("BILLING_ACCOUNT_ID must be set in environment variables.")

# Budget Alert Name
BUDGET_ALERT_NAME = os.environ.get("BUDGET_ALERT_NAME")
if not BUDGET_ALERT_NAME:
    raise ValueError("BUDGET_ALERT_NAME must be set in environment variables.")

APP_CONFIG: dict[str, Any] = {
    "monthly_budget": MONTHLY_BUDGET_AMOUNT,
    # "weekly_budget": WEEKLY_BUDGET_AMOUNT,
    # "daily_budget": DAILY_BUDGET_AMOUNT,
    "action_on_budget_reached": ACTION_ON_BUDGET_REACHED,
    "alert_on_budget_reached": ALERT_ON_BUDGET_REACHED,
    "currency_code": CURRENCY_CODE,
    "debug_mode": DEBUG_MODE,
    "billing_account_id": BILLING_ACCOUNT_ID,
    "budget_alert_name": BUDGET_ALERT_NAME,
}
