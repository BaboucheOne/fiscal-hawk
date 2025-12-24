import argparse
from pathlib import Path

from src.app import FinanceApp
from src.controller.account_controller import AccountController
from src.controller.simulation_controller import SimulationController
from src.model.account import Account
from src.model.root import Root
from src.service_locator import ServiceLocator


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--f",
        type=str,
        nargs="?",
        dest="filename",
        default="finances.yml",
        help=("Specify a yaml file with your finances."),
    )

    return parser.parse_args()


def load_user_file(filename: str) -> Root:
    file_path = Path(__file__).parent / filename
    if not Path.exists(file_path):
        print(f"File {file_path} does not exist")
        exit(-1)

    return Root.load(str(file_path))


def main(filename: str) -> None:
    root: Root = load_user_file(filename)

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
    args = read_arguments()
    main(args.filename)
