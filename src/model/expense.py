from dataclasses import dataclass


@dataclass
class Expense:
    name: str
    value: float
    date: str
    link: str
