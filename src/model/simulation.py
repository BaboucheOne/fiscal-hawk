from dataclasses import dataclass


@dataclass
class Simulation:
    runs: int
    until_year: int
    max_annual_rate: float
    min_annual_rate: float
