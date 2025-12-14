import os

from src.app import FinanceApp
from src.controller.account_controller import AccountController
from src.controller.simulation_controller import SimulationController
from src.model.account import Account
from src.model.root import Root
from src.service_locator import ServiceLocator


def load_user_file() -> Root:
    file_path = os.path.join(os.path.dirname(__file__), "finances.yml")
    return Root.load(file_path)


def main():
    root: Root = load_user_file()

    account: Account = Account(
        root.incomes,
        root.planned_expenses,
        root.expenses,
        root.market,
        root.saving_configuration,
    )

    account_controller: AccountController = AccountController(account)
    simulation_controller: SimulationController = SimulationController(root.simulation)

    ServiceLocator.register_dependency(AccountController, account_controller)
    ServiceLocator.register_dependency(SimulationController, simulation_controller)

    FinanceApp().run()


if __name__ == "__main__":
    main()
