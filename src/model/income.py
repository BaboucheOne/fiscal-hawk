from dataclasses import dataclass
from typing import Optional


@dataclass
class Income:
    name: str
    value: float
    time: str
    future_value: Optional[float] = None
    future_date: Optional[str] = None

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"value ({self.value}) must be positive")

        if self.future_value is not None and self.future_value <= 0:
            raise ValueError(f"future_value ({self.future_value}) must be positive")
