from datetime import datetime
from typing import List

from src.model.etf import Etf
from src.service.compound_interest_calculator import CompoundInterestCalculator
from src.service.monte_carlo_compound_interest_calculator import (
    MonteCarloCompoundInterestCalculator,
)
from src.model.simulation import Simulation
from src.utility import get_years_from_now


class SimulationController:

    def __init__(
        self,
        simulation: Simulation,
        compound_interest_calculator: CompoundInterestCalculator,
        monte_carlo_compound_interest_calculator: MonteCarloCompoundInterestCalculator,
    ):
        self.__simulation = simulation
        self.__compound_interest_calculator = compound_interest_calculator
        self.__monte_carlo_compound_interest_calculator = (
            monte_carlo_compound_interest_calculator
        )

    @property
    def simulation(self) -> Simulation:
        return self.__simulation

    def get_years_from_now(self):
        return get_years_from_now(self.__simulation.until_year)

    def simulate_compound_interest_on_etf(self, etf: Etf) -> List[float]:
        from_year = datetime.today().year
        return self.__compound_interest_calculator.calculate(from_year, etf)

    def simulate_monte_carlo_on_etf(self, etf: Etf) -> List[float]:
        from_year = datetime.today().year
        return self.__monte_carlo_compound_interest_calculator.calculate(from_year, etf)
