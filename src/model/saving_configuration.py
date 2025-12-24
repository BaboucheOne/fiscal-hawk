from dataclasses import dataclass
from typing import List

from src.model.saving import Saving


@dataclass
class SavingConfiguration:
    warning_percentage: int
    savings: List[Saving]

    def __post_init__(self):
        if self.warning_percentage < 0 or self.warning_percentage > 100:
            raise ValueError(
                f"warning_percentage ({self.warning_percentage}) must be between 0 and 100"
            )
