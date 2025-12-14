from dataclasses import dataclass
from typing import Optional


@dataclass
class Income:
    name: str
    value: float
    time: str
    future_value: Optional[float] = None
    future_date: Optional[str] = None
