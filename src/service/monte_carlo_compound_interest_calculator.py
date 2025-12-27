import random
import statistics
from typing import List

from src.model.account import Account
from src.model.etf import Etf
from src.model.simulation import Simulation
from src.utility import get_years, calculate_monthly_contribution


class MonteCarloCompoundInterestCalculator:
    NUMBER_OF_MONTHS_IN_YEAR: int = 12

    def __init__(self, account: Account, simulation: Simulation):
        self.__account = account
        self.__simulation = simulation

    def __monte_carlo_path(
        self,
        start_value: float,
        monthly_contribution: float,
        years: List[int],
        min_rate: float,
        max_rate: float,
    ) -> List[float]:
        value = start_value
        results: List[float] = [value]

        for _ in years:
            r = random.uniform(min_rate, max_rate)

            for _ in range(self.NUMBER_OF_MONTHS_IN_YEAR):
                value = value * (1.0 + r / self.NUMBER_OF_MONTHS_IN_YEAR) + monthly_contribution

            results.append(value)

        return results

    def calculate(self, from_year: int, etf: Etf) -> List[float]:
        year_list = get_years(from_year, self.__simulation.until_year)
        monthly_contribution: float = calculate_monthly_contribution(
            self.__account.saving_configuration.savings, etf
        )

        paths: List[List[float]] = [
            self.__monte_carlo_path(
                etf.price,
                monthly_contribution,
                year_list,
                self.__simulation.min_annual_rate,
                self.__simulation.max_annual_rate,
            )
            for _ in range(self.__simulation.runs)
        ]

        return [statistics.median(values) for values in zip(*paths)]
