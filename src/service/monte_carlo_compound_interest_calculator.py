import statistics
from typing import List

from src.model.account import Account
from src.model.etf import Etf
from src.model.simulation import Simulation
from src.utility import monte_carlo_path, get_years, calculate_monthly_contribution


class MonteCarloCompoundInterestCalculator:
    def __init__(self, account: Account, simulation: Simulation):
        self.__account = account
        self.__simulation = simulation

    def calculate(self, from_year: int, etf: Etf) -> List[float]:
        year_list = get_years(from_year, self.__simulation.until_year)
        monthly_contribution: float = calculate_monthly_contribution(
            self.__account.saving_configuration.savings, etf
        )

        paths = [
            monte_carlo_path(
                etf.price,
                monthly_contribution,
                year_list,
                self.__simulation.min_annual_rate,
                self.__simulation.max_annual_rate,
            )
            for _ in range(self.__simulation.runs)
        ]

        return [statistics.median(values) for values in zip(*paths)]
