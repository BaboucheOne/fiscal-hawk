import os

import yaml

from src.app import FinanceApp


def main():
    data_path = os.path.join(os.path.dirname(__file__), "finances.yml")
    with open(data_path, "r") as f:
        data = yaml.safe_load(f)

    FinanceApp(data).run()


if __name__ == "__main__":
    main()
