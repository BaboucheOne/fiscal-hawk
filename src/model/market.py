from dataclasses import dataclass
from typing import List

from src.model.etf import Etf
from src.model.stock import Stock


@dataclass
class Market:
    etfs: List[Etf]
    stocks: List[Stock]
