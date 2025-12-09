import os

from src.app import FinanceApp
from src.model.account import Account
from src.model.root import Root


def main():
    file_path = os.path.join(os.path.dirname(__file__), "finances.yml")
    root: Root = Root.load(file_path)

    account: Account = Account(root.incomes, root.planned_expenses, root.expenses, root.market, root.saving_configuration)

    FinanceApp(account, root.simulation).run()


if __name__ == "__main__":
    main()
