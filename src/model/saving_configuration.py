from dataclasses import dataclass
from typing import List

from src.model.saving import Saving


@dataclass
class SavingConfiguration:
    warning_percentage: int
    savings: List[Saving]
