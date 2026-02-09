"""Objects related to Project Budget / Expense / Expense Limit."""

from calendar import monthrange
from dataclasses import dataclass
from datetime import date

from helpers.constants import (
    APP_LOGGER,
    DAILY_BUDGET_AMOUNT,
    MONTHLY_BUDGET_AMOUNT,
    WEEKLY_BUDGET_AMOUNT,
)


@dataclass
class ExpenseLimit:
    """Expense Limit / Limit in Project Currency Code"""

    daily: int = DAILY_BUDGET_AMOUNT
    weekly: int = WEEKLY_BUDGET_AMOUNT
    monthly: int = MONTHLY_BUDGET_AMOUNT


@dataclass
class CurrentExpense:
    """Current Budget / Expense in Project Currency Code"""

    average_daily: float = 0.0
    average_weekly: float = 0.0
    monthly: float = 0.0


class ProjectBudget:
    """Whole Project Object that follow the limit vs the expense and check them."""

    def __init__(self) -> None:
        self.expense_limit = ExpenseLimit()
        self.current_expense = CurrentExpense()

    def check_expense_limit(self) -> bool:
        """Check the actual expense daily / weekly / monthly against the limit daily / weekly / monthly."""

        self.update_expense()
        # pylint: disable=pointless-string-statement;
        # See if we can implement daily / weekly limit.. is it interesting though?
        """
        if self.current_expense.daily >= self.expense_limit.daily:
            APP_LOGGER.warning(
                msg=f"Daily expense limit reached: {self.current_expense.daily} - Limit was: {self.expense_limit.daily}"
            )
        elif self.current_expense.weekly >= self.expense_limit.weekly:
            APP_LOGGER.warning(
                msg=f"Weekly expense limit reached: {self.current_expense.weekly} - Limit was: {self.expense_limit.weekly}"
            )
        """
        if self.current_expense.monthly >= self.expense_limit.monthly:
            APP_LOGGER.warning(
                msg=f"Monthly expense limit reached: {self.current_expense.monthly} - Limit was: {self.expense_limit.monthly}"
            )
        else:
            APP_LOGGER.info(msg="Expense limit not reached")
            return False
        return True

    def update_expense(self) -> None:
        """Update the current expense with the new values."""

        days_in_month = monthrange(date.today().year, date.today().month)[1]
        self.current_expense.average_daily = (
            self.current_expense.monthly / days_in_month
        )
        self.current_expense.average_weekly = self.current_expense.average_daily * 7
