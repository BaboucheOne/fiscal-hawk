from dataclasses import dataclass
from typing import Optional


@dataclass
class Expense:
    name: str
    value: float
    date: str
    link: Optional[str] = None

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"value ({self.value}) must be positive")
