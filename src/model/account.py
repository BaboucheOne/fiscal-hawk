from typing import List

from src.model.expense import Expense
from src.model.income import Income
from src.model.market import Market
from src.model.planned_expense import PlannedExpense
from src.model.saving_configuration import SavingConfiguration
from src.utility import yearly_adjusted_monthly_value, to_monthly


class Account:
    def __init__(
        self,
        incomes: List[Income],
        planned_expenses: List[PlannedExpense],
        expenses: List[Expense],
        market: Market,
        saving_configuration: SavingConfiguration,
    ):
        self.incomes = incomes
        self.planned_expenses = planned_expenses
        self.expenses = expenses
        self.market = market
        self.saving_configuration = saving_configuration

    def total_income(self) -> float:
        return sum(
            to_monthly(
                yearly_adjusted_monthly_value(
                    income.value, income.time, income.future_value, income.future_date
                ),
                income.time,
            )
            * 12
            for income in self.incomes
        )

    def total_planned_expenses(self) -> float:
        return sum(
            to_monthly(
                yearly_adjusted_monthly_value(
                    planned_expense.value,
                    planned_expense.time,
                    planned_expense.future_value,
                    planned_expense.future_date,
                ),
                planned_expense.time,
            )
            * 12
            for planned_expense in self.planned_expenses
        )

    def total_savings(self) -> float:
        return sum(saving.target for saving in self.saving_configuration.savings)
