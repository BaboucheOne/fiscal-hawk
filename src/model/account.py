from typing import List

from src.model.expense import Expense
from src.model.income import Income
from src.model.market import Market
from src.model.planned_expense import PlannedExpense
from src.model.saving_configuration import SavingConfiguration


class Account:
    def __init__(self, incomes: List[Income], planned_expenses: List[PlannedExpense], expenses: List[Expense], market: Market, saving_configuration: SavingConfiguration):
        self.incomes = incomes
        self.planned_expenses = planned_expenses
        self.expenses = expenses
        self.market = market
        self.saving_configuration = saving_configuration
