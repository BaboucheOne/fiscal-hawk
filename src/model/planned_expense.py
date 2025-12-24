from dataclasses import dataclass


@dataclass
class PlannedExpense:
    name: str
    value: float
    time: str

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f"value ({self.value}) must be positive")
