from typing import List

from src.model.account import Account
from src.model.expense import Expense
from src.model.income import Income
from src.model.market import Market
from src.model.planned_expense import PlannedExpense
from src.model.saving_configuration import SavingConfiguration


class AccountController:
    def __init__(self, account: Account):
        self.__account: Account = account

    @property
    def expenses(self) -> List[Expense]:
        return self.__account.expenses

    @property
    def incomes(self) -> List[Income]:
        return self.__account.incomes

    @property
    def market(self) -> Market:
        return self.__account.market

    @property
    def planned_expenses(self) -> List[PlannedExpense]:
        return self.__account.planned_expenses

    @property
    def saving_configuration(self) -> SavingConfiguration:
        return self.__account.saving_configuration
