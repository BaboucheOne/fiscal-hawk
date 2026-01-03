from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.time import Time


@dataclass
class PlannedExpense:
    name: str
    value: float
    time: Time
    future_value: Optional[float] = None
    future_date: Optional[date] = None

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"value ({self.value}) must be positive")
