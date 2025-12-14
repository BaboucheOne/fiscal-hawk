from dataclasses import dataclass
from typing import List

from src.model.etf import Etf


@dataclass
class Market:
    etfs: List[Etf]