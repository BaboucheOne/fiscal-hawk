from typing import List

from src.model.account import Account
from src.model.etf import Etf
from src.model.simulation import Simulation
from src.utility import (
    compound_interest_calculator,
    calculate_monthly_contribution,
    get_years,
)


class CompoundInterestCalculator:
    NUMBER_OF_MONTHS_IN_YEAR = 12

    def __init__(self, account: Account, simulation: Simulation):
        self.__simulation = simulation
        self.__account = account

    def calculate(self, from_year: int, etf: Etf) -> List[float]:
        years_list: List[int] = get_years(from_year, self.__simulation.until_year)

        monthly_contribution = calculate_monthly_contribution(
            self.__account.saving_configuration.savings, etf
        )

        return [
            compound_interest_calculator(
                current_value=etf.price,
                monthly_contribution=monthly_contribution,
                annual_rate=self.__simulation.max_annual_rate,
                years=year - from_year,
            )
            for year in years_list
        ]
