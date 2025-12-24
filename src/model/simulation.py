from dataclasses import dataclass


@dataclass
class Simulation:
    runs: int
    until_year: int
    max_annual_rate: float
    min_annual_rate: float

    def __post_init__(self):
        if self.runs < 1:
            raise ValueError(f"runs ({self.runs}) must be at least one.")

        if self.min_annual_rate > self.max_annual_rate:
            raise ValueError(
                f"min_annual_rate cannot ({self.min_annual_rate}) be larger than max_annual_rate ({self.max_annual_rate})"
            )
