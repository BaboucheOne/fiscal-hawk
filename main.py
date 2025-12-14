import os

from src.app import FinanceApp
from src.controller.account_controller import AccountController
from src.controller.simulation_controller import SimulationController
from src.model.account import Account
from src.model.root import Root


def main():
    file_path = os.path.join(os.path.dirname(__file__), "finances.yml")
    root: Root = Root.load(file_path)

    account: Account = Account(root.incomes, root.planned_expenses, root.expenses, root.market, root.saving_configuration)

    account_controller: AccountController = AccountController(account)
    simulation_controller: SimulationController = SimulationController(root.simulation)

    FinanceApp(account_controller, simulation_controller).run()


if __name__ == "__main__":
    main()
