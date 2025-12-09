from dataclasses import dataclass


@dataclass
class PlannedExpense:
    name: str
    value: float
    time: str